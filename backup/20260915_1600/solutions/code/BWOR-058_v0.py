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

R = dict()
R[1, 1] = 1.8
R[1, 2] = 3.2
R[1, 3] = 4.2
R[2, 1] = 2.0
R[2, 2] = 3.6
R[3, 1] = 5.4
R[3, 2] = 8.4
R[3, 3] = 12.0
R[4, 0] = 0.0
R[4, 1] = 3.2
R[4, 2] = 4.0
R[5, 1] = 3.4
R[5, 2] = 6.0
R[5, 3] = 7.2

# Decision variables
x = dict()
for i in I:
    for k in K[i]:
        x[i, k] = solver.BoolVar('x_' + str(i) + '_' + str(k))

# Objective
obj = 0
for i in I:
    for k in K[i]:
        obj += R[i, k] * x[i, k]

solver.Maximize(obj)

# Selection constraints
for i in I:
    solver.Add(sum(x[i, k] for k in K[i]) == 1)

# Area constraint
area_expr = 0
for i in I:
    for k in K[i]:
        area_expr += k * A[i] * x[i, k]

solver.Add(area_expr <= 5000)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")