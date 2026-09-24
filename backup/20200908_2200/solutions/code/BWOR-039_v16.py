from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')
x3 = solver.NumVar(0, solver.infinity(), 'x3')

# Objective function: Maximize Z = 2*x1 + 3*x2 + 1*x3
solver.Maximize(2 * x1 + 3 * x2 + 1 * x3)

# Labor constraint: x1 + x2 + x3 <= 3000
solver.Add(x1 + x2 + x3 <= 3000)

# Raw Material constraint: x1 + 4*x2 + 8*x3 <= 9000
solver.Add(x1 + 4 * x2 + 8 * x3 <= 9000)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")