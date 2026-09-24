from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Index sets
stations = [1, 2]
cities = [1, 2, 3]

# Parameters
cap = dict()
cap[1] = 400
cap[2] = 450

d_min = dict()
d_max = dict()
d_min[1] = 290
d_max[1] = 320
d_min[2] = 250
d_max[2] = 250
d_min[3] = 270
d_max[3] = 350

cost = dict()
cost[1, 1] = 15
cost[1, 2] = 18
cost[1, 3] = 22
cost[2, 1] = 21
cost[2, 2] = 25
cost[2, 3] = 16

# Decision variables: x[s, c]
x = dict()
for s in stations:
    for c in cities:
        x[s, c] = solver.NumVar(0, solver.infinity(), 'x_' + str(s) + '_' + str(c))

# Objective: minimize total cost
obj_terms = []
for s in stations:
    for c in cities:
        obj_terms.append(cost[s, c] * x[s, c])
obj = sum(obj_terms)
solver.Minimize(obj)

# Supply capacity constraints (full utilization)
for s in stations:
    expr = sum(x[s, c] for c in cities)
    solver.Add(expr == cap[s])

# Demand constraints
# City 1
solver.Add(sum(x[s, 1] for s in stations) >= d_min[1])
solver.Add(sum(x[s, 1] for s in stations) <= d_max[1])

# City 2 (fixed)
solver.Add(sum(x[s, 2] for s in stations) == d_min[2])

# City 3
solver.Add(sum(x[s, 3] for s in stations) >= d_min[3])
solver.Add(sum(x[s, 3] for s in stations) <= d_max[3])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")