from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

P = ['A', 'B', 'C']
K = [0, 1, 2, 3, 4]
F = 4

B = dict()
B[('A', 0)] = 0
B[('A', 1)] = 41
B[('A', 2)] = 48
B[('A', 3)] = 60
B[('A', 4)] = 66
B[('B', 0)] = 0
B[('B', 1)] = 42
B[('B', 2)] = 50
B[('B', 3)] = 60
B[('B', 4)] = 66
B[('C', 0)] = 0
B[('C', 1)] = 64
B[('C', 2)] = 68
B[('C', 3)] = 78
B[('C', 4)] = 76

x = dict()
for p in P:
    for k in K:
        x[p, k] = solver.BoolVar('x_' + p + '_' + str(k))

for p in P:
    solver.Add(sum(x[p, k] for k in K) == 1)

solver.Add(sum(k * x[p, k] for p in P for k in K) <= F)

obj = sum(B[p, k] * x[p, k] for p in P for k in K)
solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")