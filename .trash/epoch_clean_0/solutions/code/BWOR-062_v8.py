from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

R = [1, 2, 3]
K = [0, 1, 2, 3, 4]

P = dict()
P[1, 0] = 0
P[1, 1] = 16
P[1, 2] = 25
P[1, 3] = 30
P[1, 4] = 32
P[2, 0] = 0
P[2, 1] = 12
P[2, 2] = 17
P[2, 3] = 21
P[2, 4] = 22
P[3, 0] = 0
P[3, 1] = 10
P[3, 2] = 14
P[3, 3] = 16
P[3, 4] = 17

N = 4

x = dict()
for r in R:
    for k in K:
        x[r, k] = solver.BoolVar('x_' + str(r) + '_' + str(k))

obj = 0
for r in R:
    for k in K:
        obj += P[r, k] * x[r, k]

for r in R:
    solver.Add(sum(x[r, k] for k in K) == 1)

solver.Add(sum(k * x[r, k] for r in R for k in K) == N)

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")