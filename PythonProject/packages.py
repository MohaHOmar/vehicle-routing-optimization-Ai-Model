class Package:
    counter = 0  # Class-level counter to generate unique IDs for each package

    def __init__(self, x, y, weight, priority):
        self.destination = (x, y)
        self.weight = weight
        self.priority = priority
        self.id = Package.counter  # Assign the unique ID
        Package.counter += 1  # Increment the counter for the next package

    def __str__(self):
        return f"Destination: {self.destination}, Weight: {self.weight}, Priority: {self.priority}, ID: {self.id}"

def read_packages(filename):
    packages = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            x, y = map(float, parts[0].strip('()').split(','))
            weight = float(parts[1])
            priority = int(parts[2])
            packages.append(Package(x, y, weight, priority))  # Now creating Package without 'id' argument

    return packages
