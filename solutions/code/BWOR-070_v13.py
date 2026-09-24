from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

w = dict()
v = dict()
c = dict()

w[1] = 2
w[2] = 3
w[3] = 4
w[4] = 5

v[1] = 2
v[2] = 2
v[3] = 2
v[4] = 3

c[1] = 3
c[2] = 4
c[3] = 5
c[4] = 6

W_max = 15
V_max = 10

x = dict()
for i in range(1, 5):
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

obj = 0
for i in range(1, 5):
    obj += c[i] * x[i]

solver.Maximize(obj)

weight_expr = 0
volume_expr = 0
for i in range(1, 5):
    weight_expr += w[i] * x[i]
    volume_expr += v[i] * x[i]

solver.Add(weight_expr <= W_max)
solver.Add(volume_expr <= V_max)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")