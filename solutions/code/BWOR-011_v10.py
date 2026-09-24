from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

S = ['I', 'II']
C = [1, 2, 3]

Supply = dict()
Supply['I'] = 400
Supply['II'] = 450

Cost = dict()
Cost[('I', 1)] = 15
Cost[('I', 2)] = 18
Cost[('I', 3)] = 22
Cost[('II', 1)] = 21
Cost[('II', 2)] = 25
Cost[('II', 3)] = 16

DemandMin = dict()
DemandMin[1] = 290
DemandMin[2] = 250
DemandMin[3] = 270

DemandMax = dict()
DemandMax[1] = 320
DemandMax[2] = 250
DemandMax[3] = 350

x = dict()
for s in S:
    for c in C:
        x[s, c] = solver.NumVar(0, INF, 'x_' + s + '_' + str(c))

obj = 0
for s in S:
    for c in C:
        obj += Cost[(s, c)] * x[s, c]

solver.Minimize(obj)

for s in S:
    solver.Add(sum(x[s, c] for c in C) == Supply[s])

for c in C:
    expr = sum(x[s, c] for s in S)
    solver.Add(expr >= DemandMin[c])
    solver.Add(expr <= DemandMax[c])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")