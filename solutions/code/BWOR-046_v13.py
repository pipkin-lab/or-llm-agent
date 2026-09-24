from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

I = [1, 2, 3]
J = [1, 2, 3, 4, 5]

S = 270
U = dict()
U[1] = 50
U[2] = 100
U[3] = 150

D = dict()
D[1] = 25
D[2] = 105
D[3] = 60
D[4] = 30
D[5] = 70

C = dict()
C[1, 1] = 10
C[1, 2] = 15
C[1, 3] = 20
C[1, 4] = 20
C[1, 5] = 40
C[2, 1] = 20
C[2, 2] = 40
C[2, 3] = 15
C[2, 4] = 30
C[2, 5] = 30
C[3, 1] = 30
C[3, 2] = 35
C[3, 3] = 40
C[3, 4] = 55
C[3, 5] = 25

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

obj = 0
for i in I:
    for j in J:
        obj += C[i, j] * x[i, j]
solver.Minimize(obj)

# Supply constraint: total shipped equals production
total_ship = 0
for i in I:
    for j in J:
        total_ship += x[i, j]
solver.Add(total_ship == S)

# Warehouse capacity constraints
for i in I:
    flow_i = 0
    for j in J:
        flow_i += x[i, j]
    solver.Add(flow_i <= U[i])

# Region demand constraints
for j in J:
    flow_j = 0
    for i in I:
        flow_j += x[i, j]
    solver.Add(flow_j <= D[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")