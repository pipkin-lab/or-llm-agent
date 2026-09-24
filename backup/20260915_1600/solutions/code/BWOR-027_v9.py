import math
from ortools.linear_solver import pywraplp

# Data: city coordinates (1-indexed)
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

N = 10
cities = list(range(1, N + 1))
non_root_cities = [i for i in cities if i != 1]

# Precompute distance matrix
d = dict()
for i in cities:
    for j in cities:
        if i != j:
            xi, yi = coords[i]
            xj, yj = coords[j]
            d[i, j] = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
# x[i, j] = 1 if route goes from i to j
x = dict()
for i in cities:
    for j in cities:
        if i != j:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))

# MTZ ordering variables u[i]
u = dict()
for i in cities:
    if i == 1:
        u[i] = solver.IntVar(0, 0, 'u_{}'.format(i))
    else:
        u[i] = solver.IntVar(1, N - 1, 'u_{}'.format(i))

# Objective: minimize total distance
obj_terms = []
for i in cities:
    for j in cities:
        if i != j:
            obj_terms.append(d[i, j] * x[i, j])
solver.Minimize(sum(obj_terms))

# Constraints A: In-degree (each city entered exactly once)
for i in cities:
    in_terms = []
    for j in cities:
        if j != i:
            in_terms.append(x[j, i])
    solver.Add(sum(in_terms) == 1)

# Constraints B: Out-degree (each city exited exactly once)
for i in cities:
    out_terms = []
    for j in cities:
        if j != i:
            out_terms.append(x[i, j])
    solver.Add(sum(out_terms) == 1)

# Constraint 3: u_1 = 0 (already enforced by bounds, but add explicitly for clarity)
solver.Add(u[1] == 0)

# Constraint 5: MTZ subtour elimination for non-root cities
for i in non_root_cities:
    for j in non_root_cities:
        if i != j:
            solver.Add(u[i] - u[j] + N * x[i, j] <= N - 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")