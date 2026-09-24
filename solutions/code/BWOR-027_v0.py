import math
from ortools.linear_solver import pywraplp

# City coordinates
coords = {
    1: (0, 0),
    2: (5, 20),
    3: (8, 12),
    4: (7, 4),
    5: (10, 15),
    6: (12, 18),
    7: (18, 18),
    8: (18, 15),
    9: (18, 18),
    10: (20, 17)
}

n = 10
cities = list(range(1, n + 1))

# Calculate distances
d = dict()
for i in cities:
    for j in cities:
        if i != j:
            d[i, j] = math.sqrt((coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2)

# Initialize solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for i in cities:
    for j in cities:
        if i != j:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))

u = dict()
for i in range(2, n + 1):
    u[i] = solver.NumVar(1, n - 1, 'u_{}'.format(i))

# Objective function: minimize total distance
obj_terms = []
for i in cities:
    for j in cities:
        if i != j:
            obj_terms.append(d[i, j] * x[i, j])
solver.Minimize(sum(obj_terms))

# Constraints
# 1. Flow conservation: each city entered exactly once
for i in cities:
    expr = sum(x[j, i] for j in cities if j != i)
    solver.Add(expr == 1)

# 2. Flow conservation: each city exited exactly once
for i in cities:
    expr = sum(x[i, j] for j in cities if j != i)
    solver.Add(expr == 1)

# 3. Subtour elimination (MTZ)
for i in range(2, n + 1):
    for j in range(2, n + 1):
        if i != j:
            solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")