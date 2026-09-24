from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

projects = ['A', 'B', 'C']
levels = [0, 1, 2, 3, 4]
M = 4

R = dict()
R['A'] = {0: 0, 1: 41, 2: 48, 3: 60, 4: 66}
R['B'] = {0: 0, 1: 42, 2: 50, 3: 60, 4: 66}
R['C'] = {0: 0, 1: 64, 2: 68, 3: 78, 4: 76}

x = dict()
for p in projects:
    for k in levels:
        x[p, k] = solver.BoolVar('x_' + p + '_' + str(k))

obj = sum(R[p][k] * x[p, k] for p in projects for k in levels)
solver.Maximize(obj)

for p in projects:
    solver.Add(sum(x[p, k] for k in levels) == 1)

solver.Add(sum(k * x[p, k] for p in projects for k in levels) <= M)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")