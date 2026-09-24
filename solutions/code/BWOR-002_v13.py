from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

F = [1, 2, 3, 4, 5]
N = ['P', 'M', 'V']

a = dict()
a['P'] = dict()
a['M'] = dict()
a['V'] = dict()
a['P'][1] = 3
a['P'][2] = 2
a['P'][3] = 1
a['P'][4] = 6
a['P'][5] = 18
a['M'][1] = 1.0
a['M'][2] = 0.5
a['M'][3] = 0.2
a['M'][4] = 2.0
a['M'][5] = 0.5
a['V'][1] = 0.5
a['V'][2] = 1.0
a['V'][3] = 0.2
a['V'][4] = 2.0
a['V'][5] = 0.8

R = dict()
R['P'] = 700
R['M'] = 30
R['V'] = 100

c = dict()
c[1] = 0.2
c[2] = 0.7
c[3] = 0.4
c[4] = 0.3
c[5] = 0.8

x = dict()
for f in F:
    x[f] = solver.NumVar(0, solver.infinity(), 'x_' + str(f))

obj = 0
for f in F:
    obj += c[f] * x[f]
solver.Minimize(obj)

for n in N:
    expr = 0
    for f in F:
        expr += a[n][f] * x[f]
    solver.Add(expr >= R[n])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")