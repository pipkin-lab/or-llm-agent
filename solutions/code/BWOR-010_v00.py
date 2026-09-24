from ortools.linear_solver import pywraplp

# Decision variables x[i][j] for i in {1,2,3}, j in {1,2,3}
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

x = dict()
for i in range(1, 4):
    for j in range(1, 4):
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

# Net benefit coefficients z[i][j] = p_j - c_ij
z = dict()
z[1, 1] = 9
z[1, 2] = 6
z[1, 3] = 9
z[2, 1] = 8
z[2, 2] = 5
z[2, 3] = 3
z[3, 1] = 4
z[3, 2] = 5
z[3, 3] = 7

# Objective: maximize total net benefit
obj = 0
for i in range(1, 4):
    for j in range(1, 4):
        obj += z[i, j] * x[i, j]
solver.Maximize(obj)

# Supply constraints
supply = dict()
supply[1] = 20
supply[2] = 30
supply[3] = 20
for i in range(1, 4):
    solver.Add(sum(x[i, j] for j in range(1, 4)) <= supply[i])

# Demand constraints
demand = dict()
demand[1] = 15
demand[2] = 25
demand[3] = 20
for j in range(1, 4):
    solver.Add(sum(x[i, j] for i in range(1, 4)) <= demand[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")