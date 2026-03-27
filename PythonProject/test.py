import math
import random
import copy

# -------------------------------------- Read Input --------------------------------------

def read_vehicles(filename):
    vehicles = []
    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()
            vehicle_id = int(parts[0])
            capacity = float(parts[1])
            vehicles.append({
                "vehicle_id": vehicle_id,
                "capacity": capacity,
                "packages": [],
                "route": [],
            })
    return vehicles


def read_packages(filename):
    packages = []
    with open(filename, "r") as file:
        for i, line in enumerate(file):
            parts = line.strip().split()
            if len(parts) < 2:
                continue  # skip invalid lines
            try:
                location_str = parts[0].strip("()").replace("[", "").replace("]", "")
                x, y = map(int, location_str.split(","))
                weight = float(parts[1])
                packages.append({
                    "package_id": i + 1,
                    "location": (x, y),
                    "weight": weight
                })
            except Exception as e:
                print(f"Error reading line {i + 1}: {line.strip()} - {e}")
    return packages

# -------------------------------------- Error Handling --------------------------------------

def error_capacity(vehicles, packages):
    total_vehicle_capacity = sum(v["capacity"] for v in vehicles)
    total_package_weight = sum(p["weight"] for p in packages)
    if total_vehicle_capacity < total_package_weight:
        print("Not all the packages fit in the vehicles.")
        exit(0)

# -------------------------------------- Cost Functions --------------------------------------

def euclidean_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def total_distance(route, depot=(0, 0)):
    dist = 0
    current = depot
    for loc in route:
        dist += euclidean_distance(current, loc)
        current = loc
    dist += euclidean_distance(current, depot)
    return dist


def travel_only_cost(state):
    return sum(total_distance(v["route"]) for v in state)


def cost(state):
    total_cost = 0
    for vehicle in state:
        travel_cost = total_distance(vehicle["route"])
        total_weight = sum(p["weight"] for p in vehicle["packages"])
        capacity_penalty = 0
        if total_weight > vehicle["capacity"]:
            overload = total_weight - vehicle["capacity"]
            capacity_penalty = 1000 * overload
        total_cost += travel_cost + capacity_penalty
    return total_cost

# -------------------------------------- Initial State --------------------------------------

def routes(vehicles):
    for vehicle in vehicles:
        vehicle["route"] = [pkg["location"] for pkg in vehicle["packages"]]

def initial_state(vehicles, packages):
    vehicles_copy = copy.deepcopy(vehicles)  # <- important
    shuffled_vehicles = random.sample(vehicles_copy, len(vehicles_copy))
    shuffled_packages = random.sample(packages, len(packages))

    for package in shuffled_packages:
        assigned = False
        for vehicle in shuffled_vehicles:
            current_weight = sum(p["weight"] for p in vehicle["packages"])
            if current_weight + package["weight"] <= vehicle["capacity"]:
                vehicle["packages"].append(package)
                assigned = True
                break
        if not assigned:
            print(f"Package {package['package_id']} could not be assigned due to capacity.")

    routes(shuffled_vehicles)
    return shuffled_vehicles

# -------------------------------------- Neighbor State --------------------------------------

def neighbor(current_state):
    neighbor = copy.deepcopy(current_state)
    if len(neighbor) < 2:
        routes(neighbor)
        return neighbor

    v1, v2 = random.sample(neighbor, 2)
    op = random.choice(["swap", "move"])

    if op == "swap" and v1["packages"] and v2["packages"]:
        p1 = random.choice(v1["packages"])
        p2 = random.choice(v2["packages"])
        v1["packages"].remove(p1)
        v2["packages"].remove(p2)
        v1["packages"].append(p2)
        v2["packages"].append(p1)

    elif op == "move":
        if v1["packages"]:
            p = random.choice(v1["packages"])
            v1["packages"].remove(p)
            v2["packages"].append(p)
        elif v2["packages"]:
            p = random.choice(v2["packages"])
            v2["packages"].remove(p)
            v1["packages"].append(p)
        else:
            return neighbor

    for v in [v1, v2]:
        v["route"] = [pkg["location"] for pkg in v["packages"]]

    return neighbor

# -------------------------------------- Simulated Annealing --------------------------------------

Initial_Temperature = 1000
Cooling_Rate = 0.99
Iterations_per_Temperature = 100


def Simulated_Annealing(initial_state):
    current_state = initial_state
    best_state = copy.deepcopy(initial_state)
    T = Initial_Temperature

    while T >= 1:
        for _ in range(Iterations_per_Temperature):
            next_state = neighbor(current_state)
            delta_E = cost(next_state) - cost(current_state)

            if delta_E < 0:
                current_state = next_state
                if cost(current_state) < cost(best_state):
                    best_state = copy.deepcopy(current_state)
            else:
                probability = math.exp(-delta_E / T)
                if random.random() < probability:
                    current_state = next_state

        print(f"Temperature: {T:.2f} | Current Cost: {cost(current_state):.2f} | Best Cost: {cost(best_state):.2f}")
        T *= Cooling_Rate

    print("\n=== FINAL BEST STATE ===")
    for v in best_state:
        print(f"Vehicle {v['vehicle_id']}: Packages {[p['package_id'] for p in v['packages']]} | Route: {v['route']}")
    print(f"\nTotal Cost (Distance Only): {travel_only_cost(best_state):.2f}")
    return best_state

# -------------------------------------- Main Execution --------------------------------------

if __name__ == "__main__":
    vehicles = read_vehicles("vehicles.txt")
    packages = read_packages("packages.txt")
    error_capacity(vehicles, packages)
    initial = initial_state(vehicles, packages)
    Simulated_Annealing(initial)
