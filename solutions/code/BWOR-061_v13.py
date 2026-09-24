from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

K = [1, 2, 3, 4]

E = dict()
E[1] = 2.251
E[2] = 2.236
E[3] = 2.336
E[4] = 2.296

z = dict()
for k in K:
    z[k] = solver.IntVar(0, 1, 'z_' + str(k))

solver.Add(sum(z[k] for k in K) == 1)

obj = sum(E[k] * z[k] for k in K)
solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")