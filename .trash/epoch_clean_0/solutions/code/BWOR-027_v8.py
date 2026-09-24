import math
from ortools.linear_solver import pywraplp

# Parameters
x_coords = [0, 5, 8, 7, 10, 12, 18, 18, 18, 20]
y_coords = [0, 20, 12, 4, 15, 18, 15, 15, 18, 17]
n = 10

# Precompute distances
d = dict()
for i in range(n):
    for j in range(n):
        d[i, j] = math.sqrt((x_coords[i] - x_coords[j]) ** 2 + (y_coords[i] - y_coords[j]) ** 2)

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
# x[i, j] is binary, 1 if we travel from i to j
x = dict()
for i in range(n):
    for j in range(n):
        if i != j:
            x[i, j] = solver.IntVar(0, 1, 'x_' + str(i) + '_' + str(j))

# u[i] is continuous auxiliary variable for MTZ constraints
# u[0] is fixed to 0, so we only define u[i] for i in 1..n-1
u = dict()
for i in range(1, n):
    u[i] = solver.NumVar(0, n - 1, 'u_' + str(i))

# Objective: Minimize total distance
obj = sum(d[i, j] * x[i, j] for i in range(n) for j in range(n) if i != j)
solver.Minimize(obj)

# Constraints

# 1. Flow Conservation
for i in range(n):
    # Out-degree: sum of x[i, j] for j != i must be 1
    solver.Add(sum(x[i, j] for j in range(n) if j != i) == 1)
    # In-degree: sum of x[j, i] for j != i must be 1
    solver.Add(sum(x[j, i] for j in range(n) if j != i) == 1)

# 2. Subtour Elimination (MTZ)
# u[0] is implicitly 0.
# For i, j in 1..n-1, i != j:
# u[i] - u[j] + n * x[i, j] <= n - 1
for i in range(1, n):
    for j in range(1, n):
        if i != j:
            solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")