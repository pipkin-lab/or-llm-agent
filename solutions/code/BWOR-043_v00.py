from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
supply = dict()
supply[1] = 50
supply[2] = 40
supply[3] = 60
supply[4] = 31

demand = dict()
demand[1] = 30
demand[2] = 50
demand[3] = 20
demand[4] = 40
demand[5] = 30
demand[6] = 11

cost = dict()
cost[1, 1] = 2
cost[1, 2] = 1
cost[1, 3] = 3
cost[1, 4] = 3
cost[1, 5] = 3
cost[1, 6] = 5
cost[2, 1] = 4
cost[2, 2] = 2
cost[2, 3] = 2
cost[2, 4] = 4
cost[2, 5] = 4
cost[2, 6] = 4
cost[3, 1] = 3
cost[3, 2] = 5
cost[3, 3] = 4
cost[3, 4] = 2
cost[3, 5] = 4
cost[3, 6] = 1
cost[4, 1] = 4
cost[4, 2] = 2
cost[4, 3] = 2
cost[4, 4] = 1
cost[4, 5] = 2
cost[4, 6] = 2

origins = [1, 2, 3, 4]
destinations = [1, 2, 3, 4, 5, 6]

# Decision variables x[i, j]
x = dict()
for i in origins:
    for j in destinations:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

# Objective: minimize total cost
obj_terms = []
for i in origins:
    for j in destinations:
        obj_terms.append(cost[i, j] * x[i, j])
solver.Minimize(sum(obj_terms))

# Supply constraints
for i in origins:
    solver.Add(sum(x[i, j] for j in destinations) == supply[i])

# Demand constraints
for j in destinations:
    solver.Add(sum(x[i, j] for i in origins) == demand[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")