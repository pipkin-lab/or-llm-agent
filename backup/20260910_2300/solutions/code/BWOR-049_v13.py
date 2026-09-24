from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
x_X_A = solver.NumVar(0, solver.infinity(), 'x_X_A')
x_X_B = solver.NumVar(0, solver.infinity(), 'x_X_B')
x_X_C = solver.NumVar(0, solver.infinity(), 'x_X_C')
x_Y_A = solver.NumVar(0, solver.infinity(), 'x_Y_A')
x_Y_B = solver.NumVar(0, solver.infinity(), 'x_Y_B')
x_Y_C = solver.NumVar(0, solver.infinity(), 'x_Y_C')
x_A_B = solver.NumVar(0, solver.infinity(), 'x_A_B')
x_A_C = solver.NumVar(0, solver.infinity(), 'x_A_C')
x_B_A = solver.NumVar(0, solver.infinity(), 'x_B_A')
x_B_C = solver.NumVar(0, solver.infinity(), 'x_B_C')
x_C_A = solver.NumVar(0, solver.infinity(), 'x_C_A')
x_C_B = solver.NumVar(0, solver.infinity(), 'x_C_B')

# Objective function
solver.Minimize(10 * x_X_A + 14 * x_X_B + 12 * x_X_C + 15 * x_Y_A + 12 * x_Y_B + 18 * x_Y_C + 14 * x_A_B + 11 * x_A_C + 10 * x_B_A + 4 * x_B_C + 8 * x_C_A + 12 * x_C_B)

# Supply constraints
solver.Add(x_X_A + x_X_B + x_X_C == 70)
solver.Add(x_Y_A + x_Y_B + x_Y_C == 55)

# Demand/transshipment flow-balance constraints
solver.Add(x_X_A + x_Y_A + x_B_A + x_C_A - x_A_B - x_A_C == 35)
solver.Add(x_X_B + x_Y_B + x_A_B + x_C_B - x_B_A - x_B_C == 40)
solver.Add(x_X_C + x_Y_C + x_A_C + x_B_C - x_C_A - x_C_B == 50)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")