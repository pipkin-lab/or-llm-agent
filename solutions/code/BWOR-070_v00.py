from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x_1, x_2, x_3, x_4 (non-negative integers)
x = dict()
for i in range(1, 5):
    x[i] = solver.IntVar(0, INF, 'x_' + str(i))

# Objective: Maximize Z = 3x1 + 4x2 + 5x3 + 6x4
obj = 3 * x[1] + 4 * x[2] + 5 * x[3] + 6 * x[4]
solver.Maximize(obj)

# Constraint 1 (Weight): 2x1 + 3x2 + 4x3 + 5x4 <= 15
solver.Add(2 * x[1] + 3 * x[2] + 4 * x[3] + 5 * x[4] <= 15)

# Constraint 2 (Volume): 2x1 + 2x2 + 2x3 + 3x4 <= 10
solver.Add(2 * x[1] + 2 * x[2] + 2 * x[3] + 3 * x[4] <= 10)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")