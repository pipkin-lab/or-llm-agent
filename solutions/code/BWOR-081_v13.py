from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

x1 = solver.NumVar(0, INF, 'x1')
x2 = solver.NumVar(0, INF, 'x2')

# Raw Material A: 1*x1 + 2*x2 <= 6000
solver.Add(1 * x1 + 2 * x2 <= 6000)

# Raw Material B: 2*x1 + 1*x2 <= 8000
solver.Add(2 * x1 + 1 * x2 <= 8000)

# Market Demand Limit for Product II: x2 <= 2
solver.Add(x2 <= 2)

# Relative Sales Constraint: x2 - x1 <= 1
solver.Add(x2 - x1 <= 1)

# Objective: Maximize 30*x1 + 20*x2
solver.Maximize(30 * x1 + 20 * x2)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")