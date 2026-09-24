from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

stations = [1, 2]
cities = [1, 2, 3]

x = dict()
for i in stations:
    for j in cities:
        x[i, j] = solver.NumVar(0, INF, 'x_{}{}'.format(i, j))

# Objective
cost = dict()
cost[1, 1] = 15
cost[1, 2] = 18
cost[1, 3] = 22
cost[2, 1] = 21
cost[2, 2] = 25
cost[2, 3] = 16

obj = 0
for i in stations:
    for j in cities:
        obj += cost[i, j] * x[i, j]

# Supply constraints
solver.Add(x[1, 1] + x[1, 2] + x[1, 3] == 400)
solver.Add(x[2, 1] + x[2, 2] + x[2, 3] == 450)

# Demand constraints
# City 1: 290 <= x11 + x21 <= 320
solver.Add(x[1, 1] + x[2, 1] >= 290)
solver.Add(x[1, 1] + x[2, 1] <= 320)

# City 2: x12 + x22 = 250
solver.Add(x[1, 2] + x[2, 2] == 250)

# City 3: 270 <= x13 + x23 <= 350
solver.Add(x[1, 3] + x[2, 3] >= 270)
solver.Add(x[1, 3] + x[2, 3] <= 350)

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")