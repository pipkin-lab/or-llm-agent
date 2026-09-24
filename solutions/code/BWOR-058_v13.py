from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index sets
I = [1, 2, 3, 4, 5]
K = dict()
K[1] = [1, 2, 3]
K[2] = [1, 2]
K[3] = [1, 2, 3]
K[4] = [0, 1, 2]
K[5] = [1, 2, 3]

# Parameters
A = dict()
A[1] = 250
A[2] = 350
A[3] = 800
A[4] = 400
A[5] = 500

Rent = dict()
Rent[1, 1] = 1.8
Rent[1, 2] = 3.2
Rent[1, 3] = 4.2
Rent[2, 1] = 2.0
Rent[2, 2] = 3.6
Rent[3, 1] = 5.4
Rent[3, 2] = 8.4
Rent[3, 3] = 12.0
Rent[4, 0] = 0.0
Rent[4, 1] = 3.2
Rent[4, 2] = 4.0
Rent[5, 1] = 3.4
Rent[5, 2] = 6.0
Rent[5, 3] = 7.2

Area_total = 5000

# Decision variables
z = dict()
for i in I:
    for k in K[i]:
        z[i, k] = solver.BoolVar('z_' + str(i) + '_' + str(k))

# Objective: Maximize total rental income
obj = 0
for i in I:
    for k in K[i]:
        obj += Rent[i, k] * z[i, k]
solver.Maximize(obj)

# Constraint: Exactly one count per store type
for i in I:
    solver.Add(sum(z[i, k] for k in K[i]) == 1)

# Constraint: Total area
area_expr = 0
for i in I:
    for k in K[i]:
        area_expr += k * A[i] * z[i, k]
solver.Add(area_expr <= Area_total)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")