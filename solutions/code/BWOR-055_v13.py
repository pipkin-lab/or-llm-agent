from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

products = [1, 2, 3]

x = dict()
y = dict()

for i in products:
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))
    y[i] = solver.BoolVar('y_' + str(i))

M = dict()
M[1] = 40
M[2] = 53
M[3] = 25

for i in products:
    solver.Add(x[i] <= M[i] * y[i])

labor_per_unit = dict()
labor_per_unit[1] = 3
labor_per_unit[2] = 2
labor_per_unit[3] = 6

mat_per_unit = dict()
mat_per_unit[1] = 4
mat_per_unit[2] = 3
mat_per_unit[3] = 6

L_total = 150
M_total = 160

solver.Add(sum(labor_per_unit[i] * x[i] for i in products) <= L_total)
solver.Add(sum(mat_per_unit[i] * x[i] for i in products) <= M_total)

m = dict()
m[1] = 60
m[2] = 40
m[3] = 100

F = dict()
F[1] = 2000
F[2] = 1500
F[3] = 1000

obj = sum(m[i] * x[i] for i in products) - sum(F[i] * y[i] for i in products)
solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")