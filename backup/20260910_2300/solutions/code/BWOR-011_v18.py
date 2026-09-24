from ortools.linear_solver import pywraplp

# Model Type: LP
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: x[i][j] for i in {I, II}, j in {1, 2, 3}
stations = ['I', 'II']
cities = [1, 2, 3]

x = dict()
for i in stations:
    for j in cities:
        x[i, j] = solver.NumVar(0, INF, 'x_%s_%d' % (i, j))

# Objective: Minimize total cost
cost = dict()
cost[('I', 1)] = 15
cost[('I', 2)] = 18
cost[('I', 3)] = 22
cost[('II', 1)] = 21
cost[('II', 2)] = 25
cost[('II', 3)] = 16

objective = 0
for i in stations:
    for j in cities:
        objective += cost[(i, j)] * x[i, j]

solver.Minimize(objective)

# Supply constraints (full utilization)
supply = dict()
supply['I'] = 400
supply['II'] = 450

for i in stations:
    solver.Add(sum(x[i, j] for j in cities) == supply[i])

# Demand constraints
# City 1: 290 <= x[I,1] + x[II,1] <= 320
solver.Add(x['I', 1] + x['II', 1] >= 290)
solver.Add(x['I', 1] + x['II', 1] <= 320)

# City 2: x[I,2] + x[II,2] = 250
solver.Add(x['I', 2] + x['II', 2] == 250)

# City 3: 270 <= x[I,3] + x[II,3] <= 350
solver.Add(x['I', 3] + x['II', 3] >= 270)
solver.Add(x['I', 3] + x['II', 3] <= 350)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")