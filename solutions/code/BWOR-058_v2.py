from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index sets
J = [1, 2, 3, 4, 5]

# Parameters
A_total = 5000
r = 0.20
a = dict()
a[1] = 250
a[2] = 350
a[3] = 800
a[4] = 400
a[5] = 500

L = dict()
L[1] = 1
L[2] = 1
L[3] = 1
L[4] = 0
L[5] = 1

U = dict()
U[1] = 3
U[2] = 2
U[3] = 3
U[4] = 2
U[5] = 3

# Profit p[k][m]: annual profit per store of type k when exactly m stores are leased
p = dict()
p[1] = dict()
p[1][0] = 0
p[1][1] = 9
p[1][2] = 8
p[1][3] = 7

p[2] = dict()
p[2][0] = 0
p[2][1] = 10
p[2][2] = 9

p[3] = dict()
p[3][0] = 0
p[3][1] = 27
p[3][2] = 21
p[3][3] = 20

p[4] = dict()
p[4][0] = 0
p[4][1] = 16
p[4][2] = 10

p[5] = dict()
p[5][0] = 0
p[5][1] = 17
p[5][2] = 15
p[5][3] = 12

# Decision variables: y[k][m] is 1 if exactly m stores of type k are leased
y = dict()
for k in J:
    y[k] = dict()
    for m in range(0, U[k] + 1):
        y[k][m] = solver.BoolVar('y_' + str(k) + '_' + str(m))

# Objective function: Maximize total rental income
obj = 0
for k in J:
    for m in range(0, U[k] + 1):
        obj += r * m * p[k][m] * y[k][m]

solver.Maximize(obj)

# Constraints
# A. Selection constraints: exactly one count per type
for k in J:
    expr = 0
    for m in range(0, U[k] + 1):
        expr += y[k][m]
    solver.Add(expr == 1)

# B. Minimum store requirements: y[k][0] = 0 for types with L[k] >= 1
for k in J:
    if L[k] >= 1:
        solver.Add(y[k][0] == 0)

# C. Total area constraint
area_expr = 0
for k in J:
    for m in range(0, U[k] + 1):
        area_expr += m * a[k] * y[k][m]
solver.Add(area_expr <= A_total)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")