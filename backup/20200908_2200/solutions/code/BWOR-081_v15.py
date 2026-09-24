from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')

# Objective: Maximize Z = 30*x1 + 20*x2
solver.Maximize(30 * x1 + 20 * x2)

# Constraint 1: Raw Material A: 1*x1 + 2*x2 <= 6
solver.Add(1 * x1 + 2 * x2 <= 6)

# Constraint 2: Raw Material B: 2*x1 + 1*x2 <= 8
solver.Add(2 * x1 + 1 * x2 <= 8)

# Constraint 3: Market Demand Limit for Product II: x2 <= 2
solver.Add(x2 <= 2)

# Constraint 4: Sales Balance: x2 - x1 <= 1
solver.Add(x2 - x1 <= 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")