import math
from ortools.linear_solver import pywraplp

# Data: City coordinates (1-indexed in the model, 0-indexed in Python)
# City 1: (0, 0)
# City 2: (5, 20)
# City 3: (8, 12)
# City 4: (7, 4)
# City 5: (10, 15)
# City 6: (12, 18)
# City 7: (18, 18)
# City 8: (18, 15)
# City 9: (18, 18)
# City 10: (20, 17)

coords = dict()
coords[1] = (0, 0)
coords[2] = (5, 20)
coords[3] = (8, 12)
coords[4] = (7, 4)
coords[5] = (10, 15)
coords[6] = (12, 18)
coords[7] = (18, 18)
coords[8] = (18, 15)
coords[9] = (18, 18)
coords[10] = (20, 17)

n = 10
cities = range(1, n + 1)

# Precompute distances
d = dict()
for i in cities:
    for j in cities:
        if i != j:
            xi, yi = coords[i]
            xj, yj = coords[j]
            d[i, j] = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[i, j]
x = dict()
for i in cities:
    for j in cities:
        if i != j:
            x[i, j] = solver.IntVar(0, 1, 'x_' + str(i) + '_' + str(j))

# Auxiliary variables u[i] for MTZ
u = dict()
for i in cities:
    u[i] = solver.NumVar(0, n - 1, 'u_' + str(i))

# Objective function: Minimize total distance
obj_terms = []
for i in cities:
    for j in cities:
        if i != j:
            obj_terms.append(d[i, j] * x[i, j])
solver.Minimize(sum(obj_terms))

# Constraints

# 1. Flow conservation: out-degree = 1 for each city
for i in cities:
    solver.Add(sum(x[i, j] for j in cities if j != i) == 1)

# 2. Flow conservation: in-degree = 1 for each city
for j in cities:
    solver.Add(sum(x[i, j] for i in cities if i != j) == 1)

# 3. MTZ subtour elimination constraints: u[i] - u[j] + n * x[i, j] <= n - 1
# Applied for all i, j where i != j.
# Note: The standard MTZ formulation is applied for all arcs.
# We also fix u[1] = 0 as per the model.
solver.Add(u[1] == 0)

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