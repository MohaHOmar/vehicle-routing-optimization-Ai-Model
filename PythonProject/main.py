from vehicles import read_vehicles
from packages import read_packages
from simulated_annealing import run_simulated_annealing
from genetic_algorithm import run_genetic_algorithm, calculate_total_distance
from plot import plot_vehicle_routes_live

def print_menu():
    print("\n=== Local Package Delivery Optimization ===")
    print("1. Load Data")
    print("2. Run Simulated Annealing")
    print("3. Run Genetic Algorithm")
    print("4. Show Vehicles & Packages")
    print("5. Exit")

def main():
    vehicles = []
    packages = []

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        match choice:
            case '1':
                vehicles = read_vehicles('vehicles.txt')
                packages = read_packages('packages.txt')
                print(f"Loaded {len(vehicles)} vehicles and {len(packages)} packages.")

            case '2':
                best_solution = run_simulated_annealing(packages, vehicles)
                best_cost = calculate_total_distance(best_solution)
                plot_vehicle_routes_live(best_solution,best_cost)
            case '3':

                best_solution = run_genetic_algorithm(packages, vehicles)
                best_cost = calculate_total_distance(best_solution)
                print(f"Best Total Distance (Cost): {best_cost:.2f}")


                for vehicle in best_solution:
                    print(vehicle)
                    for p in vehicle.packages:
                        print(f"  - {p}")
                plot_vehicle_routes_live(best_solution,best_cost)

            case '5':
                print("Goodbye!")
                break

            case _:
                print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
