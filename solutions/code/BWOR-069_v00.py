from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: non-negative integers
x1 = solver.IntVar(0, solver.infinity(), 'x1')
x2 = solver.IntVar(0, solver.infinity(), 'x2')
x3 = solver.IntVar(0, solver.infinity(), 'x3')

# Transportation capacity constraint
solver.Add(2 * x1 + 3 * x2 + 4 * x3 <= 10)

# Objective function: maximize total profit
objective = 100 * x1 + 140 * x2 + 180 * x3
solver.Maximize(objective)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")