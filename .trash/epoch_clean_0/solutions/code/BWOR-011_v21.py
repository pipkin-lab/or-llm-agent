from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables x[i][j], i in {1,2}, j in {1,2,3}
x = dict()
for i in [1, 2]:
    for j in [1, 2, 3]:
        x[i, j] = solver.NumVar(0, INF, 'x_{}_{}'.format(i, j))

# Parameters
c = dict()
c[1, 1] = 15
c[1, 2] = 18
c[1, 3] = 22
c[2, 1] = 21
c[2, 2] = 25
c[2, 3] = 16

S = dict()
S[1] = 400
S[2] = 450

L = dict()
L[1] = 290
L[2] = 250
L[3] = 270

U = dict()
U[1] = 320
U[2] = 250
U[3] = 350

# Objective
obj = 0
for i in [1, 2]:
    for j in [1, 2, 3]:
        obj += c[i, j] * x[i, j]
solver.Minimize(obj)

# Supply constraints (equality)
for i in [1, 2]:
    solver.Add(sum(x[i, j] for j in [1, 2, 3]) == S[i])

# Demand constraints
for j in [1, 2, 3]:
    demand_expr = sum(x[i, j] for i in [1, 2])
    solver.Add(demand_expr >= L[j])
    solver.Add(demand_expr <= U[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")