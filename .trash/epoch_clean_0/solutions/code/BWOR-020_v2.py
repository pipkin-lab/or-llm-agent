from ortools.linear_solver import pywraplp

# Define the problem
solver = pywraplp.Solver.CreateSolver('SCIP')

# Sets
C = ['A', 'B', 'C', 'D', 'E']
T = [1, 2, 3, 4]

# Parameters
d = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 8}
K = {1: 2, 2: 6, 3: 8, 4: 11}
c = {1: 1, 2: 2, 3: 3, 4: 4}  # Assuming cost coefficients are 1, 2, 3, 4 since not specified

# Decision Variables
x = dict()
for i in C:
    for j in T:
        x[i, j] = solver.BoolVar('x_%s_%d' % (i, j))

y = dict()
for j in T:
    y[j] = solver.BoolVar('y_%d' % j)

# Objective Function
obj = sum(c[j] * y[j] for j in T)
solver.Minimize(obj)

# Constraints

# 1. Demand Satisfaction: Each customer must be served by exactly one truck
for i in C:
    solver.Add(sum(x[i, j] for j in T) == 1)

# 2. Truck Capacity Constraints
for j in T:
    solver.Add(sum(d[i] * x[i, j] for i in C) <= K[j] * y[j])

# 3. Linking Constraints: Truck usage
for j in T:
    solver.Add(sum(x[i, j] for i in C) <= y[j])

# 4. Incompatibility Constraints
# Truck j cannot serve both Customer A and Customer C
for j in T:
    solver.Add(x['A', j] + x['C', j] <= 1)

# Truck j cannot serve both Customer B and Customer D
for j in T:
    solver.Add(x['B', j] + x['D', j] <= 1)

# Solve the problem
status = solver.Solve()

# Output the result
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")