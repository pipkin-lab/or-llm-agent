from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

T = [1, 2, 3]

D = {1: 3, 2: 3, 3: 3}
capN = {1: 2, 2: 4, 3: 1}
capO = {1: 3, 2: 2, 3: 3}
costN = {1: 500, 2: 600, 3: 550}
costO = {1: 570, 2: 670, 3: 620}
h = 40
I0 = 2
Ifinal = 1

xN = dict()
xO = dict()
I = dict()
for t in T:
    xN[t] = solver.IntVar(0, INF, 'xN_' + str(t))
    xO[t] = solver.IntVar(0, INF, 'xO_' + str(t))
    I[t] = solver.IntVar(0, INF, 'I_' + str(t))

obj = 0
for t in T:
    obj += costN[t] * xN[t]
    obj += costO[t] * xO[t]
    obj += h * I[t]
solver.Minimize(obj)

for t in T:
    solver.Add(xN[t] <= capN[t])
    solver.Add(xO[t] <= capO[t])

for t in T:
    prev = I0 if t == 1 else I[t - 1]
    solver.Add(prev + xN[t] + xO[t] - I[t] == D[t])

solver.Add(I[3] == Ifinal)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")