from ortools.linear_solver import pywraplp

# Initialize the MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    raise RuntimeError("SCIP solver not available")

INF = solver.infinity()

# Decision variables
# x_j: continuous production quantity for product j (j = 1, 2, 3)
x = dict()
for j in range(1, 4):
    x[j] = solver.NumVar(0, INF, 'x_' + str(j))

# y_j: binary indicator for producing product j
y = dict()
for j in range(1, 4):
    y[j] = solver.BoolVar('y_' + str(j))

# Objective: Maximize Z = 4x1 + 5x2 + 6x3 - 100y1 - 150y2 - 200y3
objective = 4 * x[1] + 5 * x[2] + 6 * x[3] - 100 * y[1] - 150 * y[2] - 200 * y[3]
solver.Maximize(objective)

# Resource constraints
# Resource A: 2x1 + 4x2 + 8x3 <= 500
solver.Add(2 * x[1] + 4 * x[2] + 8 * x[3] <= 500)

# Resource B: 2x1 + 3x2 + 4x3 <= 300
solver.Add(2 * x[1] + 3 * x[2] + 4 * x[3] <= 300)

# Resource C: 1x1 + 2x2 + 3x3 <= 100
solver.Add(1 * x[1] + 2 * x[2] + 3 * x[3] <= 100)

# Big-M linking constraints
# x1 <= 100 * y1
solver.Add(x[1] <= 100 * y[1])

# x2 <= 50 * y2
solver.Add(x[2] <= 50 * y[2])

# x3 <= (100/3) * y3
solver.Add(x[3] <= (100 / 3) * y[3])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")