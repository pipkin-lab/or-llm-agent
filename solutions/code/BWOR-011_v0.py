from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

stations = ['I', 'II']
cities = [1, 2, 3]

cap = dict()
cap['I'] = 400
cap['II'] = 450

dmin = dict()
dmin[1] = 290
dmin[2] = 250
dmin[3] = 270

dmax = dict()
dmax[1] = 320
dmax[2] = 250
dmax[3] = 350

cost = dict()
cost[('I', 1)] = 15
cost[('I', 2)] = 18
cost[('I', 3)] = 22
cost[('II', 1)] = 21
cost[('II', 2)] = 25
cost[('II', 3)] = 16

x = dict()
for s in stations:
    for j in cities:
        x[s, j] = solver.NumVar(0, INF, 'x_' + s + '_' + str(j))

obj = 0
for s in stations:
    for j in cities:
        obj += cost[(s, j)] * x[s, j]

solver.Minimize(obj)

for s in stations:
    solver.Add(sum(x[s, j] for j in cities) == cap[s])

for j in cities:
    solver.Add(sum(x[s, j] for s in stations) >= dmin[j])
    solver.Add(sum(x[s, j] for s in stations) <= dmax[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")