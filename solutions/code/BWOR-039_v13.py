from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

x = dict()
x[1] = solver.NumVar(0, INF, 'x_1')
x[2] = solver.NumVar(0, INF, 'x_2')
x[3] = solver.NumVar(0, INF, 'x_3')

p = dict()
p[1] = 2
p[2] = 3
p[3] = 1

a = dict()
a[1] = 1.0 / 30.0
a[2] = 1.0 / 30.0
a[3] = 1.0 / 30.0

b = dict()
b[1] = 10.0 / 3.0
b[2] = 40.0 / 3.0
b[3] = 80.0 / 3.0

L = 100
M = 30000

indices = [1, 2, 3]

solver.Add(sum(a[i] * x[i] for i in indices) <= L)
solver.Add(sum(b[i] * x[i] for i in indices) <= M)

obj = sum(p[i] * x[i] for i in indices)
solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")