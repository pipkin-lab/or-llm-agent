from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

machines = ['A', 'B', 'C', 'D']

f = dict()
f['A'] = 1000
f['B'] = 920
f['C'] = 800
f['D'] = 700

c = dict()
c['A'] = 20
c['B'] = 24
c['C'] = 16
c['D'] = 28

U = dict()
U['A'] = 900
U['B'] = 1000
U['C'] = 1200
U['D'] = 1600

D = 2000

x = dict()
y = dict()
for i in machines:
    x[i] = solver.NumVar(0, INF, 'x_' + i)
    y[i] = solver.BoolVar('y_' + i)

solver.Add(sum(x[i] for i in machines) == D)

for i in machines:
    solver.Add(x[i] <= U[i] * y[i])

obj = sum(f[i] * y[i] + c[i] * x[i] for i in machines)
solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")