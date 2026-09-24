from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets
I = [1, 2, 3]
J = [1, 2, 3, 4, 5]

# Parameters
S = 270
C = dict()
C[1] = 50
C[2] = 100
C[3] = 150

D = dict()
D[1] = 25
D[2] = 105
D[3] = 60
D[4] = 30
D[5] = 70

c = dict()
c[1, 1] = 10
c[1, 2] = 15
c[1, 3] = 20
c[1, 4] = 20
c[1, 5] = 40
c[2, 1] = 20
c[2, 2] = 40
c[2, 3] = 15
c[2, 4] = 30
c[2, 5] = 30
c[3, 1] = 30
c[3, 2] = 35
c[3, 3] = 40
c[3, 4] = 55
c[3, 5] = 25

# Decision variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

# Objective
obj = sum(c[i, j] * x[i, j] for i in I for j in J)
solver.Minimize(obj)

# Supply constraint (equality)
solver.Add(sum(x[i, j] for i in I for j in J) == S)

# Warehouse capacity constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= C[i])

# Regional demand constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) <= D[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")