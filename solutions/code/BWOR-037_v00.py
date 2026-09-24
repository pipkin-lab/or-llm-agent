from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x_1a = solver.IntVar(0, INF, 'x_1a')
x_1b = solver.IntVar(0, INF, 'x_1b')
x_2a = solver.IntVar(0, INF, 'x_2a')
x_2b = solver.IntVar(0, INF, 'x_2b')
x_3a = solver.IntVar(0, INF, 'x_3a')
x_3b = solver.IntVar(0, INF, 'x_3b')

# Objective function
solver.Minimize(100 * x_1a + 260 * x_1b + 100 * x_2a + 80 * x_2b + 400 * x_3a + 340 * x_3b)

# Constraints
solver.Add(x_1a + x_1b + x_2a + x_3b <= 400)
solver.Add(2 * x_1b + x_2b + 5 * x_3a + 3 * x_3b <= 800)
solver.Add(42 * x_1a + 114 * x_1b >= 10000)
solver.Add(42 * x_2a + 36 * x_2b >= 20000)
solver.Add(180 * x_3a + 150 * x_3b >= 30000)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")