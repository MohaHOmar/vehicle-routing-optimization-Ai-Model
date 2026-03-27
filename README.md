# 🚚 Delivery Optimization using Metaheuristics

An optimization system that simulates and improves package delivery routing using **Genetic Algorithm** and **Simulated Annealing**.

The goal is to minimize total delivery cost (distance + priority penalties) while respecting vehicle constraints.

---

## 🚀 Overview
This project models a real-world **vehicle routing problem (VRP)** where:
- Packages must be assigned to vehicles  
- Vehicles have limited capacity  
- Delivery routes should be optimized  

Two metaheuristic algorithms are used:
- 🧬 Genetic Algorithm (GA)  
- 🌡️ Simulated Annealing (SA)  

---

## 🎯 Objective
Minimize:
- 🚗 Total travel distance  
- ⚠️ Priority penalties (late delivery of important packages)  

While satisfying:
- Vehicle capacity constraints  
- All packages must be delivered  

---

## 🧠 Algorithms

### 🔹 Simulated Annealing
- Starts with a random solution  
- Iteratively improves via:
  - Move (transfer package)
  - Swap (exchange packages)  
- Uses temperature-based exploration  

#### ⚙️ Key Parameters
- Initial Temperature: 1000  
- Cooling Rate: 0.99  
- Iterations per step: 100  

---

### 🔹 Genetic Algorithm
- Population-based optimization  
- Uses:
  - Selection  
  - Crossover  
  - Mutation  

#### ⚙️ Key Parameters
- Population Size: 50  
- Mutation Rate: 0.05  
- Generations: 500  

---

## 📊 Problem Modeling

### 📦 Input
- Package list:
  - Coordinates  
  - Weight  
  - Priority  

- Vehicles:
  - Capacity  

---

### 📤 Output
- Assignment of packages to vehicles  
- Optimized delivery routes  
- Total cost  

---

## 📏 Cost Function: Total Cost = Distance + Priority Penalty


- Distance → Euclidean distance  
- Priority penalty → penalizes late delivery of high-priority packages  

---

## 🔧 Constraints
- Vehicle capacity must not be exceeded  
- All packages must be assigned  
- Invalid solutions are rejected  

---

## 📈 Features
- Dynamic input (vehicles & packages)  
- Multiple test cases  
- Graphical visualization of routes  
- Comparison between two optimization algorithms  

---

👨‍💻 Author

Mohammad Omar
