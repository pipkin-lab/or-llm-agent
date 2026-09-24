from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Index sets
I = range(3)  # Warehouses 0, 1, 2
J = range(5)  # Regions 0, 1, 2, 3, 4

# Parameters
S = 270
W = [50, 100, 150]
D = [25, 105, 60, 30, 70]

# Cost matrix C[i][j]
C = [
    [10, 15, 20, 20, 40],  # Warehouse A1
    [20, 40, 15, 30, 30],  # Warehouse A2
    [30, 35, 40, 55, 25]   # Warehouse A3
]

# Decision variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

# Objective function
obj = sum(C[i][j] * x[i, j] for i in I for j in J)
solver.Minimize(obj)

# Constraints

# 1. Warehouse Capacity Constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= W[i])

# 2. Region Demand Constraints (upper bounds)
for j in J:
    solver.Add(sum(x[i, j] for i in I) <= D[j])

# 3. Supply Constraint (all produced sugar must be distributed)
solver.Add(sum(x[i, j] for i in I for j in J) == S)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")