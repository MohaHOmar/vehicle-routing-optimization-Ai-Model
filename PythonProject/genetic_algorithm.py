import random
import math
import copy

from vehicles import Vehicle


def check_size(packages, vehicles):
    """
     Verifies if the total vehicle capacity can accommodate all package weights.
     Also ensures no package exceeds the max capacity of any individual vehicle.
     """
    total_package_weight = 0
    for pkg in packages:
        total_package_weight += pkg.weight

    total_vehicle_capacity = 0
    for v in vehicles:
        total_vehicle_capacity += v.capacity

    if total_package_weight > total_vehicle_capacity:
        print("The vehicles are not enough to carry all the packages!")
        exit()

    max_vehicle_capacity = max(v.capacity for v in vehicles)
    oversized_packages = []
    for pkg in packages:
        if pkg.weight > max_vehicle_capacity:
            oversized_packages.append(pkg)

    if oversized_packages:
        for pkg in oversized_packages:
            print(
                f"The package (Weight: {pkg.weight} kg, Priority: {pkg.priority}, Location: {pkg.destination}) is too heavy for any vehicle! ")
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

def initial_population(packages, vehicles, population_size):
    """
    Creates an initial random population of feasible package-to-vehicle assignments.
    """
    population = []

    for _ in range(population_size):
        my_packages = packages[:]
        random.shuffle(my_packages)

        vehicles_copy = []
        for v in vehicles:
            new_vehicle = Vehicle(v.id, v.capacity)
            vehicles_copy.append(new_vehicle)

        for pkg in my_packages:
            assigned = False
            vehicle_ids = list(range(len(vehicles_copy)))
            random.shuffle(vehicle_ids)

            for i in vehicle_ids:
                if vehicles_copy[i].add_package(pkg):
                    assigned = True
                    break

        population.append(vehicles_copy)

    return population

def fitness(solution):
    """
    Defines fitness as the negative of total cost (since we aim to minimize cost).
    """
    return -calculate_total_distance(solution)


def selection(population, fitnesses, tournament_size=3):
    """
    Tournament selection: Randomly selects individuals and returns the best among them.
    """
    selected_indices = random.sample(range(len(population)), tournament_size)

    selected_fitnesses = []
    selected_population = []

    for i in selected_indices:
        selected_fitnesses.append(fitnesses[i])
        selected_population.append(population[i])

    winner_index = selected_fitnesses.index(max(selected_fitnesses))
    return selected_population[winner_index]


def remove_duplicates(vehicles):
    """
    Ensures that each package is assigned to only one vehicle (prevents duplication after crossover).
    """

    seen = set()
    for v in vehicles:
        unique_packages = []
        for p in v.packages:
            if p.id not in seen:
                unique_packages.append(p)
                seen.add(p.id)
        v.packages = unique_packages


def crossover(chromosome1, chromosome2):
    """
    Performs crossover between two parent solutions and generates two children:
    - Mixes vehicles from both parents
    - Removes duplicates and fills missing packages
    """
    parent1 = copy.deepcopy(chromosome1)
    parent2 = copy.deepcopy(chromosome2)

    if parent1 != parent2:
        cross_point = random.randint(1, len(parent1) - 1)
        child1_vehicles = []
        child2_vehicles = []

        for i in range(cross_point):
            child1_vehicles.append(parent1[i])
            child2_vehicles.append(parent2[i])
        for i in range(cross_point, len(parent1)):
            child1_vehicles.append(parent2[i])
            child2_vehicles.append(parent1[i])

        remove_duplicates(child1_vehicles)
        remove_duplicates(child2_vehicles)

        assigned_nums = set()
        for v in child1_vehicles:
            for p in v.packages:
                assigned_nums.add(p.id)

        all_packages = {}
        for v in chromosome1 + chromosome2:
            for p in v.packages:
                all_packages[p.id] = p

        missing_packages = []
        for num, p in all_packages.items():
            if num not in assigned_nums:
                missing_packages.append(p)

        for pkg in missing_packages:
            random.shuffle(child1_vehicles)
            for v in child1_vehicles:
                if v.current_load() + pkg.weight <= v.capacity:
                    v.add_package(pkg)
                    break

        assigned_nums = set()
        for v in child2_vehicles:
            for p in v.packages:
                assigned_nums.add(p.id)

        missing_packages = []
        for num, p in all_packages.items():
            if num not in assigned_nums:
                missing_packages.append(p)

        for pkg in missing_packages:
            random.shuffle(child2_vehicles)
            for v in child2_vehicles:
                if v.current_load() + pkg.weight <= v.capacity:
                    v.add_package(pkg)
                    break

        parent1 = child1_vehicles
        parent2 = child2_vehicles

    return parent1, parent2


def mutate(solution, mutation_rate):
    """
    Mutates a solution by:
    - Randomly moving a package from one vehicle to another
    - Or swapping two packages with the same priority between vehicles
    """
    new_vehicles = copy.deepcopy(solution)
    active_vehicles = []

    for v in new_vehicles:
        if v.packages:
            active_vehicles.append(v)

    if len(active_vehicles) < 2:
        return new_vehicles

    if random.random() < mutation_rate:
        operation = random.choice(['move', 'swap'])

        if operation == 'move':
            v_from = random.choice(active_vehicles)
            selected_package = random.choice(v_from.packages)

            target_vehicles = []
            for v in new_vehicles:
                if v != v_from and v.current_load() + selected_package.weight <= v.capacity:
                    target_vehicles.append(v)

            if target_vehicles:
                v_to = random.choice(target_vehicles)
                v_from.packages.remove(selected_package)
                v_to.packages.append(selected_package)

        elif operation == 'swap':
            v1, v2 = random.sample(active_vehicles, 2)
            p1 = random.choice(v1.packages)

            swappable_p2s = []
            for p2 in v2.packages:
                if p2.priority == p1.priority:
                    swappable_p2s.append(p2)

            if swappable_p2s:
                p2 = random.choice(swappable_p2s)

                if (v1.current_load() - p1.weight + p2.weight <= v1.capacity and
                        v2.current_load() - p2.weight + p1.weight <= v2.capacity):
                    v1.packages.remove(p1)
                    v2.packages.remove(p2)
                    v1.packages.append(p2)
                    v2.packages.append(p1)

    return new_vehicles
def check_num(max_test,individual):
    """
    Ensures that the number of packages in the individual matches the expected max (i.e., no loss during crossover/mutation).
    """
    max_pkg_num = 0
    for vehicle in individual:
        max_pkg_num += len(vehicle.packages)
    if (max_pkg_num == max_test):
        return True
    else:
        return False

def run_genetic_algorithm(packages, vehicles, population_size=50, mutation_rate=0.05, generations=500):
    """
    Main loop for running the genetic algorithm:
    - Initializes a random population
    - Evolves the population through selection, crossover, and mutation
    - Keeps track of the best solution found
    """
    check_size(packages, vehicles)
    population = initial_population(packages, vehicles, population_size)
    max_test = 0
    max_pkg_num = 0
    for i in population:
        for vehicle in i:
            max_pkg_num += len(vehicle.packages)
        if(max_pkg_num > max_test):
            max_test = max_pkg_num
        max_pkg_num = 0

    best_solution = None
    best_fitness = float('-inf')

    for gen in range(generations):
        fitnesses = []
        for ind in population:
            fitnesses.append(fitness(ind))

        gen_best = max(fitnesses)

        if gen_best > best_fitness:
            best_fitness = gen_best
            best_solution = copy.deepcopy(population[fitnesses.index(gen_best)])

        print(f"Generation {gen}, Best Fitness: {gen_best:.2f}")

        new_population = []
        for _ in range(population_size // 2):
            parent1 = copy.deepcopy(selection(population, fitnesses))
            parent2 = copy.deepcopy(selection(population, fitnesses))
            child1, child2 = crossover(parent1, parent2)

            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)

            if check_num(max_test, child1):
                new_population.append(child1)
            if check_num(max_test, child2):
                new_population.append(child2)

        new_population.sort(key=lambda x: fitness(x))
        population = new_population
    actual_cost = calculate_total_distance_and_real_cost(best_solution)
    total_cost = calculate_total_distance(best_solution)
    print(f"\nActual Cost (without penalty): {actual_cost:.2f}")
    print(f"Total Cost (with penalty): {total_cost:.2f}")

    return best_solution
