from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

S = [1, 2, 3, 4, 5, 6]
T = [1, 2, 3, 4, 5, 6]

R = dict()
R[1] = 10
R[2] = 15
R[3] = 25
R[4] = 20
R[5] = 18
R[6] = 12

w_F = 10
w_C = 15
H = 8
C_F = w_F * H
C_C = w_C * H

a = dict()
for t in T:
    for s in S:
        a[t, s] = 0

a[1, 1] = 1
a[2, 1] = 1
a[2, 2] = 1
a[3, 2] = 1
a[3, 3] = 1
a[4, 3] = 1
a[4, 4] = 1
a[5, 4] = 1
a[5, 5] = 1
a[6, 5] = 1
a[6, 6] = 1
a[1, 6] = 1

x_F = dict()
for s in S:
    x_F[s] = solver.IntVar(0, solver.infinity(), 'x_F_' + str(s))

x_C = dict()
for s in S:
    x_C[s] = solver.IntVar(0, solver.infinity(), 'x_C_' + str(s))

obj = 0
for s in S:
    obj += C_F * x_F[s] + C_C * x_C[s]

solver.Minimize(obj)

for t in T:
    expr = 0
    for s in S:
        expr += a[t, s] * (x_F[s] + x_C[s])
    solver.Add(expr >= R[t])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")