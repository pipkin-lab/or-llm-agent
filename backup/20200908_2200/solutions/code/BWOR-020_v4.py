from ortools.linear_solver import pywraplp

# Define the problem
solver = pywraplp.Solver.CreateSolver('SCIP')

# Data
customers = ['A', 'B', 'C', 'D', 'E']
trucks = [1, 2, 3, 4]

demand = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 8}
capacity = {1: 2, 2: 6, 3: 8, 4: 11}

# Costs are symbolic in the problem statement.
# Since no specific values are provided, we use a placeholder value of 1 for each truck.
# In a real scenario, these would be specific numerical values.
cost = {1: 1, 2: 1, 3: 1, 4: 1}

# Decision Variables
# x[i, j] = 1 if customer i is assigned to truck j
x = {}
for i in customers:
    for j in trucks:
        x[i, j] = solver.BoolVar('x_' + i + '_' + str(j))

# y[j] = 1 if truck j is used
y = {}
for j in trucks:
    y[j] = solver.BoolVar('y_' + str(j))

# Objective Function: Minimize total cost
objective = 0
for j in trucks:
    objective += cost[j] * y[j]

solver.Minimize(objective)

# Constraints

# A. Customer Service Constraints: Each customer served exactly once
for i in customers:
    solver.Add(sum(x[i, j] for j in trucks) == 1)

# B. Truck Capacity Constraints
for j in trucks:
    solver.Add(sum(demand[i] * x[i, j] for i in customers) <= capacity[j])

# C. Linking Constraints: x[i, j] <= y[j]
for i in customers:
    for j in trucks:
        solver.Add(x[i, j] <= y[j])

# D. Compatibility Constraints
# 1. A truck cannot deliver to both Customer A and Customer C
for j in trucks:
    solver.Add(x['A', j] + x['C', j] <= 1)

# 2. A truck cannot deliver to both Customer B and Customer D
for j in trucks:
    solver.Add(x['B', j] + x['D', j] <= 1)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")