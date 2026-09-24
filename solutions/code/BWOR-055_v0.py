from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Parameters
products = [1, 2, 3]
m = dict()
F = dict()
a = dict()
b = dict()
U = dict()

m[1] = 60
m[2] = 40
m[3] = 100

F[1] = 2000
F[2] = 1500
F[3] = 1000

a[1] = 3
a[2] = 2
a[3] = 6

b[1] = 4
b[2] = 3
b[3] = 6

U[1] = 40
U[2] = 53
U[3] = 25

L_max = 150
M_max = 160

# Variables
x = dict()
y = dict()
for i in products:
    x[i] = solver.IntVar(0, INF, 'x_' + str(i))
    y[i] = solver.BoolVar('y_' + str(i))

# Objective
obj = 0
for i in products:
    obj += m[i] * x[i]
    obj -= F[i] * y[i]
solver.Maximize(obj)

# Labor constraint
solver.Add(a[1] * x[1] + a[2] * x[2] + a[3] * x[3] <= L_max)

# Material constraint
solver.Add(b[1] * x[1] + b[2] * x[2] + b[3] * x[3] <= M_max)

# Linking constraints
for i in products:
    solver.Add(x[i] <= U[i] * y[i])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")