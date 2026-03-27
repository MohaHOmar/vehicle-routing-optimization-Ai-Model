class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.packages = []

    def current_load(self):
        return sum(p.weight for p in self.packages)

    def add_package(self, package):
        if self.current_load() + package.weight <= self.capacity:
            self.packages.append(package)
            return True
        return False


    def __str__(self):
        return f"Vehicle {self.id} | Capacity: {self.capacity} | Packages: {len(self.packages)}"

def read_vehicles(filename):
    vehicles = []
    with open(filename, 'r') as f:
        for idx, line in enumerate(f):
            capacity = int(line.strip())

            vehicles.append(Vehicle(idx, capacity))

    return vehicles