from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

INF = solver.infinity()

# Decision variables
x = dict()
y = dict()
for p in [1, 2, 3]:
    x[p] = solver.NumVar(0, INF, 'x_' + str(p))
    y[p] = solver.BoolVar('y_' + str(p))

# Parameters
m = dict()
F = dict()
m[1] = 4
m[2] = 5
m[3] = 6
F[1] = 100
F[2] = 150
F[3] = 200

# Objective: maximize contribution margin minus fixed costs
obj = m[1] * x[1] + m[2] * x[2] + m[3] * x[3] - F[1] * y[1] - F[2] * y[2] - F[3] * y[3]
solver.Maximize(obj)

# Resource constraints
# Resource A: 2x1 + 4x2 + 8x3 <= 500
solver.Add(2 * x[1] + 4 * x[2] + 8 * x[3] <= 500)
# Resource B: 2x1 + 3x2 + 4x3 <= 300
solver.Add(2 * x[1] + 3 * x[2] + 4 * x[3] <= 300)
# Resource C: x1 + 2x2 + 3x3 <= 100
solver.Add(1 * x[1] + 2 * x[2] + 3 * x[3] <= 100)

# Linking constraints (Big-M)
solver.Add(x[1] <= 100 * y[1])
solver.Add(x[2] <= 50 * y[2])
solver.Add(x[3] <= 33.34 * y[3])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")