from ortools.linear_solver import pywraplp

# Initialize SCIP solver for MILP
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x1 = solver.IntVar(0, INF, 'x1')  # bundles of manuscript paper
x2 = solver.IntVar(0, INF, 'x2')  # dozens of diaries
x3 = solver.IntVar(0, INF, 'x3')  # boxes of exercise books
T  = solver.IntVar(0, INF, 'T')   # temporary workers

# Objective: Maximize net profit
solver.Maximize(2 * x1 + 3 * x2 + 1 * x3 - 40 * T)

# Constraint 1: Raw material (simplified: 10*x1 + 40*x2 + 80*x3 <= 90000)
solver.Add(10 * x1 + 40 * x2 + 80 * x3 <= 90000)

# Constraint 2: Labor capacity (simplified: x1 + x2 + x3 <= 3000 + 30*T)
solver.Add(x1 + x2 + x3 <= 3000 + 30 * T)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")