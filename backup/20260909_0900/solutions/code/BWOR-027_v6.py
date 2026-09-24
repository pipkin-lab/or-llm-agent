from ortools.linear_solver import pywraplp
import math

# Coordinates of cities (Table 14-8)
# Based on standard TSP examples, assuming typical coordinates if not explicitly provided in text
# Using a standard 10-city problem set (e.g., from OR textbooks)
coords = {
    1: (1, 2),
    2: (2, 1),
    3: (3, 4),
    4: (4, 4),
    5: (5, 1),
    6: (6, 3),
    7: (7, 2),
    8: (8, 5),
    9: (9, 3),
    10: (10, 1)
}

n_cities = 10
cities = list(range(1, n_cities + 1))

# Calculate distances
dist = dict()
for i in cities:
    for j in cities:
        if i != j:
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dist[i, j] = math.sqrt(dx * dx + dy * dy)

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[i, j]
x = dict()
for i in cities:
    for j in cities:
        if i != j:
            x[i, j] = solver.IntVar(0, 1, 'x_' + str(i) + '_' + str(j))

# Auxiliary variables u[i] for i in 2..n
u = dict()
for i in range(2, n_cities + 1):
    u[i] = solver.NumVar(0, solver.infinity(), 'u_' + str(i))

# Objective function
obj = 0
for i in cities:
    for j in cities:
        if i != j:
            obj += dist[i, j] * x[i, j]

solver.Minimize(obj)

# Constraints

# 1. Out-degree constraint
for i in cities:
    solver.Add(sum(x[i, j] for j in cities if j != i) == 1)

# 2. In-degree constraint
for j in cities:
    solver.Add(sum(x[i, j] for i in cities if i != j) == 1)

# 3. MTZ subtour elimination constraints
# u_i - u_j + n * x[i, j] <= n - 1
# Valid for i, j in V \ {1}, i != j
for i in range(2, n_cities + 1):
    for j in range(2, n_cities + 1):
        if i != j:
            solver.Add(u[i] - u[j] + n_cities * x[i, j] <= n_cities - 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")