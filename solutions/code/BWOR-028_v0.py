from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

INF = solver.infinity()

# Decision variables: x_s for s = 1..6 (integer, non-negative)
x = dict()
for s in range(1, 7):
    x[s] = solver.IntVar(0, INF, 'x_' + str(s))

# Demand parameters
d = dict()
d[1] = 12
d[2] = 10
d[3] = 15
d[4] = 25
d[5] = 20
d[6] = 18

# Coverage matrix a[t][s]
a = dict()
a[1] = dict()
a[1][1] = 1
a[1][2] = 0
a[1][3] = 0
a[1][4] = 0
a[1][5] = 0
a[1][6] = 1

a[2] = dict()
a[2][1] = 1
a[2][2] = 1
a[2][3] = 0
a[2][4] = 0
a[2][5] = 0
a[2][6] = 0

a[3] = dict()
a[3][1] = 0
a[3][2] = 1
a[3][3] = 1
a[3][4] = 0
a[3][5] = 0
a[3][6] = 0

a[4] = dict()
a[4][1] = 0
a[4][2] = 0
a[4][3] = 1
a[4][4] = 1
a[4][5] = 0
a[4][6] = 0

a[5] = dict()
a[5][1] = 0
a[5][2] = 0
a[5][3] = 0
a[5][4] = 1
a[5][5] = 1
a[5][6] = 0

a[6] = dict()
a[6][1] = 0
a[6][2] = 0
a[6][3] = 0
a[6][4] = 0
a[6][5] = 1
a[6][6] = 1

# Coverage constraints
for t in range(1, 7):
    expr = sum(a[t][s] * x[s] for s in range(1, 7))
    solver.Add(expr >= d[t])

# Objective: minimize total nurses
obj = sum(x[s] for s in range(1, 7))
solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")