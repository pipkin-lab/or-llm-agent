from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

w = dict()
w[1] = 2
w[2] = 3
w[3] = 4

p = dict()
p[1] = 100
p[2] = 140
p[3] = 180

W = 10

x = dict()
for i in range(1, 4):
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

solver.Add(w[1] * x[1] + w[2] * x[2] + w[3] * x[3] <= W)

obj = p[1] * x[1] + p[2] * x[2] + p[3] * x[3]
solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")