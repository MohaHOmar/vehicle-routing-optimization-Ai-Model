import random
import math
import copy

# Verifies that the total package weight does not exceed total vehicle capacity.
# Also checks if any individual package is too heavy for the most capable vehicle.
# Exits the program if delivery is not feasible.
def check_size(packages, vehicles):
    total_package_weight = sum(pkg.weight for pkg in packages)
    total_vehicle_capacity = sum(v.capacity for v in vehicles)

    if total_package_weight > total_vehicle_capacity:
        print("The vehicles are not enough to carry all the packages!")
        exit()

    max_vehicle_capacity = max(v.capacity for v in vehicles)
    oversized_packages = [pkg for pkg in packages if pkg.weight > max_vehicle_capacity]
    if oversized_packages:
        for pkg in oversized_packages:
            print(f"The package (Weight: {pkg.weight} kg, Priority: {pkg.priority}, Location: {pkg.destination}) is too heavy for any vehicle!")
        exit()



def calculate_total_distance(vehicles):
    """
    Calculates the total cost of the solution:
    - Sum of Euclidean distances for round-trip routes (shop → destinations → shop)
    - Plus a weighted priority penalty (late deliveries of high-priority packages)
    """
    lambda_param = 0.3
    total_distance = 0
    priority_penalty = 0
    shop = (0, 0)

    for vehicle in vehicles:
        if not vehicle.packages:
            continue

        # Build route: Shop → each destination → back to shop
        route = [shop] + [p.destination for p in vehicle.packages]

        # Sum distances for full round trip
        for i in range(len(route) - 1):
            total_distance += math.dist(route[i], route[i + 1])

        # Add priority penalty (weighted by delivery position)
        for idx, package in enumerate(vehicle.packages):
            priority_penalty += package.priority * (idx + 1)

    total = total_distance + lambda_param * priority_penalty
    return total



def calculate_total_distance_and_real_cost(vehicles):
    """
    Calculates the total cost of the solution:
    - Sum of Euclidean distances for round-trip routes (shop → destinations → shop)
    - Plus a weighted priority penalty (late deliveries of high-priority packages)
    """
    lambda_param = 0.3
    total_distance = 0
    priority_penalty = 0
    shop = (0, 0)

    for vehicle in vehicles:
        if not vehicle.packages:
            continue

        # Build route: Shop → each destination → back to shop
        route = [shop] + [p.destination for p in vehicle.packages]

        # Sum distances for full round trip
        for i in range(len(route) - 1):
            total_distance += math.dist(route[i], route[i + 1])
    return total_distance



# Creates a neighboring solution (small variation of current solution) by randomly
# either moving a package from one vehicle to another or swapping packages between vehicles.
# Ensures vehicle capacity constraints are not violated during changes.
def create_neighbor_solution(vehicles):
    new_vehicles = copy.deepcopy(vehicles)
    active_vehicles = [v for v in new_vehicles if v.packages]
    if len(active_vehicles) < 2:
        return new_vehicles

    operation = random.choice(['swap', 'move'])

    if operation == 'move':
        v_from = random.choice(active_vehicles)
        p = random.choice(v_from.packages)
        target_vehicles = [v for v in new_vehicles if v != v_from and v.current_load() + p.weight <= v.capacity]
        if not target_vehicles:
            return new_vehicles
        v_to = random.choice(target_vehicles)
        v_from.packages.remove(p)
        v_to.packages.append(p)

    elif operation == 'swap':
        v1, v2 = random.sample(active_vehicles, 2)
        p1 = random.choice(v1.packages)
        swappable_p2s = [p2 for p2 in v2.packages if p2.priority == p1.priority]
        if not swappable_p2s:
            return new_vehicles
        p2 = random.choice(swappable_p2s)
        if (v1.current_load() - p1.weight + p2.weight <= v1.capacity and
                v2.current_load() - p2.weight + p1.weight <= v2.capacity):
            v1.packages.remove(p1)
            v2.packages.remove(p2)
            v1.packages.append(p2)
            v2.packages.append(p1)

    return new_vehicles


# Attempts to distribute all packages to vehicles randomly but feasibly (within capacity limits).
# Retries up to 100 times if a valid assignment isn't found. Returns initial and best solution.
def distribute_packages(packages, vehicles):
    check_size(packages, vehicles)

    max_retries = 100  # Prevent infinite loops
    for attempt in range(max_retries):
        unassigned_packages = packages[:]
        random.shuffle(unassigned_packages)
        vehicles_copy = copy.deepcopy(vehicles)

        success = True

        for pkg in unassigned_packages:
            assigned = False
            for v in vehicles_copy:
                if v.current_load() + pkg.weight <= v.capacity:
                    v.add_package(pkg)
                    assigned = True
                    break
            if not assigned:
                success = False
                break  # Restart whole assignment attempt

        if success:
            current_solution = vehicles_copy
            best_solution = copy.deepcopy(current_solution)
            current_cost = calculate_total_distance(current_solution)
            best_cost = current_cost
            return current_solution, best_solution, current_cost, best_cost

    raise RuntimeError("Failed to assign all packages after multiple retries.")


# Runs the Simulated Annealing algorithm to find an optimized assignment of packages to vehicles.
# Uses temperature-based probabilistic acceptance of worse solutions to avoid local minima.
# Restarts with a new distribution if stuck for 10 consecutive temperature drops.
# Returns the best found vehicle-package assignment.
def run_simulated_annealing(packages, vehicles):
    current_solution, best_solution, current_cost, best_cost = distribute_packages(packages, vehicles)
    T = 1000
    cooling_rate = 0.99
    stopping_temperature = 1
    iterations_per_temperature = 100
    stuck_counter = 0

    while T > stopping_temperature:
        improved = False
        for _ in range(iterations_per_temperature):
            neighbor_solution = create_neighbor_solution(current_solution)
            neighbor_cost = calculate_total_distance(neighbor_solution)
            delta_e = neighbor_cost - current_cost

            if delta_e < 0 or random.random() < math.exp(-delta_e / T):
                # if check_num(max_test,neighbor_solution):
                current_solution = neighbor_solution
                current_cost = neighbor_cost
                if current_cost < best_cost:
                    best_solution = copy.deepcopy(current_solution)
                    best_cost = current_cost
                    improved = True

        if not improved:
            stuck_counter += 1
        else:
            stuck_counter = 0

        if stuck_counter >= 10:
            print("\n[RESTART] Stuck, redistributing packages...\n")
            new_current, _, new_cost, _ = distribute_packages(packages, vehicles)
            if new_cost < best_cost:
                print(f"→ New redistributed cost is better: {new_cost:.2f} < {best_cost:.2f}")
                current_solution = new_current
                current_cost = new_cost
                best_solution = copy.deepcopy(current_solution)
                best_cost = current_cost
                T = 1000  # Reset temperature
            stuck_counter = 0

        T *= cooling_rate
        print(f"Temp: {T:.2f} | Current Cost: {current_cost:.2f} | Best Cost: {best_cost:.2f}")

    print("\n=== Best Found Assignment ===")
    for v in best_solution:
        print(v)
        for p in v.packages:
            print(f"   - {p}")

    # Uncomment to visualize if you have a GUI or plotting backend
    # plot_vehicle_routes_live(best_solution, best_cost)

    # Get and print both actual cost and total cost (with penalty)
    actual_cost = calculate_total_distance_and_real_cost(best_solution)
    total_cost= calculate_total_distance(best_solution)
    print(f"\nActual Cost (without penalty): {actual_cost:.2f}")
    print(f"Total Cost (with penalty): {total_cost:.2f}")

    return best_solution
