from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

origins = [1, 2, 3]
destinations = [1, 2, 3, 4, 5]

cost = dict()
cost[(1, 1)] = 10
cost[(1, 2)] = 15
cost[(1, 3)] = 20
cost[(1, 4)] = 20
cost[(1, 5)] = 40
cost[(2, 1)] = 20
cost[(2, 2)] = 10
cost[(2, 3)] = 15
cost[(2, 4)] = 30
cost[(2, 5)] = 30
cost[(3, 1)] = 30
cost[(3, 2)] = 35
cost[(3, 3)] = 40
cost[(3, 4)] = 55
cost[(3, 5)] = 25

supply = dict()
supply[1] = 50
supply[2] = 100
supply[3] = 150

demand = dict()
demand[1] = 25
demand[2] = 115
demand[3] = 60
demand[4] = 30
demand[5] = 70

x = dict()
for i in origins:
    for j in destinations:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

obj = sum(cost[i, j] * x[i, j] for i in origins for j in destinations)
solver.Minimize(obj)

for i in origins:
    solver.Add(sum(x[i, j] for j in destinations) <= supply[i])

for j in destinations:
    solver.Add(sum(x[i, j] for i in origins) >= demand[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")