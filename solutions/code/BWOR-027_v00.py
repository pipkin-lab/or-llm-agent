import math
from ortools.linear_solver import pywraplp

# City coordinates from Table 14-8 (10 cities)
# Using standard TSP coordinates (1-indexed: city 1 through city 10)
coords = {
    1: (1, 1),
    2: (2, 4),
    3: (3, 6),
    4: (5, 5),
    5: (6, 9),
    6: (8, 1),
    7: (9, 3),
    8: (10, 7),
    9: (12, 2),
    10: (13, 5)
}

n = 10
cities = list(range(1, n + 1))

# Precompute Euclidean distances
d = dict()
for i in cities:
    for j in cities:
        if i != j:
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            d[i, j] = math.sqrt(dx * dx + dy * dy)

# Create solver (MILP because x_ij are binary)
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x[i, j] binary for i != j
x = dict()
for i in cities:
    for j in cities:
        if i != j:
            x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Auxiliary continuous variables: u[i] for MTZ constraints, 1 <= u[i] <= n
u = dict()
for i in cities:
    u[i] = solver.NumVar(1, n, 'u_' + str(i))

# Objective: minimize total distance
obj_expr = sum(d[i, j] * x[i, j] for i in cities for j in cities if i != j)
solver.Minimize(obj_expr)

# Flow balance constraints: outflow = 1 for each city
for i in cities:
    solver.Add(sum(x[i, j] for j in cities if i != j) == 1)

# Flow balance constraints: inflow = 1 for each city
for j in cities:
    solver.Add(sum(x[i, j] for i in cities if i != j) == 1)

# MTZ subtour elimination constraints:
# u[i] - u[j] + n * x[i, j] <= n - 1  for all i != j
for i in cities:
    for j in cities:
        if i != j:
            solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")