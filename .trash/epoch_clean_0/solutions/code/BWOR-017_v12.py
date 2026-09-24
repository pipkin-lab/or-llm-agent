from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    raise RuntimeError("Could not create solver")

# Parameters
I = [1, 2, 3]

b = {}
b['A'] = 500
b['B'] = 300
b['C'] = 100

# a[j][i] = unit consumption of resource j for product i
a = {}
a['A'] = {1: 2, 2: 4, 3: 8}
a['B'] = {1: 2, 2: 3, 3: 4}
a['C'] = {1: 1, 2: 2, 3: 3}

c = {1: 4, 2: 5, 3: 6}
f = {1: 100, 2: 150, 3: 200}

# Big-M values
M = {1: 100, 2: 50, 3: 100.0 / 3.0}

# Decision variables
x = dict()
y = dict()
for i in I:
    x[i] = solver.NumVar(0, solver.infinity(), 'x_' + str(i))
    y[i] = solver.BoolVar('y_' + str(i))

# Linking constraints: x_i <= M_i * y_i
for i in I:
    solver.Add(x[i] <= M[i] * y[i])

# Resource constraints
solver.Add(a['A'][1] * x[1] + a['A'][2] * x[2] + a['A'][3] * x[3] <= b['A'])
solver.Add(a['B'][1] * x[1] + a['B'][2] * x[2] + a['B'][3] * x[3] <= b['B'])
solver.Add(a['C'][1] * x[1] + a['C'][2] * x[2] + a['C'][3] * x[3] <= b['C'])

# Objective function: Maximize sum(c_i * x_i - f_i * y_i)
obj = sum(c[i] * x[i] - f[i] * y[i] for i in I)
solver.Maximize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")