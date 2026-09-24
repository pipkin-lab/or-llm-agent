from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x_A = solver.NumVar(0, INF, 'x_A')
x_B = solver.NumVar(0, INF, 'x_B')
x_C = solver.NumVar(0, INF, 'x_C')

# Objective: Maximize total return
solver.Maximize(0.05 * x_A + 0.07 * x_B + 0.10 * x_C)

# Constraint 1: Minimum investment in A
solver.Add(x_A >= 300)

# Constraint 2: Maximum share per product (35% of 1000 = 350)
solver.Add(x_A <= 350)
solver.Add(x_B <= 350)
solver.Add(x_C <= 350)

# Constraint 3: Total investment limit (1000 - 100 emergency reserve = 900)
solver.Add(x_A + x_B + x_C <= 900)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")