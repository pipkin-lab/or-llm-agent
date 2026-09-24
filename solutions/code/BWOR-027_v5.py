import math
from ortools.linear_solver import pywraplp

# City coordinates (1-indexed)
cities = list(range(1, 11))
x_coord = {1: 0, 2: 5, 3: 8, 4: 7, 5: 10, 6: 12, 7: 18, 8: 18, 9: 18, 10: 20}
y_coord = {1: 0, 2: 20, 3: 12, 4: 4, 5: 15, 6: 18, 7: 18, 8: 15, 9: 18, 10: 17}

N = len(cities)

# Pre-compute Euclidean distances
c = dict()
for i in cities:
    for j in cities:
        if i != j:
            c[i, j] = math.sqrt((x_coord[i] - x_coord[j]) ** 2 + (y_coord[i] - y_coord[j]) ** 2)

# Create MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for i in cities:
    for j in cities:
        if i != j:
            x[i, j] = solver.BoolVar('x_%d_%d' % (i, j))

# Auxiliary variables for MTZ subtour elimination
u = dict()
for k in cities:
    if k == 1:
        u[k] = solver.NumVar(0, 0, 'u_%d' % k)
    else:
        u[k] = solver.NumVar(0, N - 1, 'u_%d' % k)

# Objective: minimize total distance
objective_terms = []
for i in cities:
    for j in cities:
        if i != j:
            objective_terms.append(c[i, j] * x[i, j])
solver.Minimize(sum(objective_terms))

# Flow conservation: outflow
for i in cities:
    outflow_terms = []
    for j in cities:
        if j != i:
            outflow_terms.append(x[i, j])
    solver.Add(sum(outflow_terms) == 1)

# Flow conservation: inflow
for j in cities:
    inflow_terms = []
    for i in cities:
        if i != j:
            inflow_terms.append(x[i, j])
    solver.Add(sum(inflow_terms) == 1)

# MTZ subtour elimination constraints
for i in cities:
    for j in cities:
        if i != j:
            solver.Add(u[i] - u[j] + N * x[i, j] <= N - 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")