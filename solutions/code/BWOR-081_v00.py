from ortools.linear_solver import pywraplp

# Create the LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Define decision variables (continuous, non-negative)
x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')

# Objective function: Maximize Z = 30*x1 + 20*x2
solver.Maximize(30 * x1 + 20 * x2)

# Constraint: Raw Material A: x1 + 2*x2 <= 6
solver.Add(x1 + 2 * x2 <= 6)

# Constraint: Raw Material B: 2*x1 + x2 <= 8
solver.Add(2 * x1 + x2 <= 8)

# Constraint: Market limit for Product II: x2 <= 2
solver.Add(x2 <= 2)

# Constraint: Relative sales: -x1 + x2 <= 1
solver.Add(-x1 + x2 <= 1)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")