from ortools.linear_solver import pywraplp

# Parameters
I = [1, 2, 3, 4]
J = [1, 2, 3, 4]
K = [3, 4]

S = dict()
S[1] = 400
S[2] = 600
S[3] = 200
S[4] = 200

D = dict()
D[1] = 350
D[2] = 400
D[3] = 300
D[4] = 150

c = dict()
c[1, 1] = 2
c[1, 2] = 9
c[1, 3] = 3
c[1, 4] = 4
c[2, 1] = 8
c[2, 2] = 3
c[2, 3] = 5
c[2, 4] = 7
c[3, 1] = 7
c[3, 2] = 6
c[3, 3] = 1
c[3, 4] = 2
c[4, 1] = 4
c[4, 2] = 5
c[4, 3] = 2
c[4, 4] = 5

F = dict()
F[3] = 1200
F[4] = 1500

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

y = dict()
for k in K:
    y[k] = solver.IntVar(0, 1, 'y_' + str(k))

# Objective
obj = 0
for i in I:
    for j in J:
        obj += c[i, j] * x[i, j]
for k in K:
    obj += F[k] * y[k]

solver.Minimize(obj)

# Supply capacity constraints
for i in I:
    if i in K:
        solver.Add(sum(x[i, j] for j in J) <= S[i] * y[i])
    else:
        solver.Add(sum(x[i, j] for j in J) <= S[i])

# Demand satisfaction constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

# Single-facility selection constraint
solver.Add(y[3] + y[4] == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")