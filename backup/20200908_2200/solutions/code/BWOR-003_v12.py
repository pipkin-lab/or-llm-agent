from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
D = [0, 100, 150, 120, 110]  # D[1] to D[4]
r_bank = 1.04
R_A = 1.40
R_B = 1.25
R_C = 1.30
U_A = 60
U_B = 90
U_C = 50

# Decision Variables (continuous, non-negative)
F = solver.NumVar(0, solver.infinity(), 'F')
x_A = solver.NumVar(0, solver.infinity(), 'x_A')
x_B = solver.NumVar(0, solver.infinity(), 'x_B')
x_C = solver.NumVar(0, solver.infinity(), 'x_C')
y_1 = solver.NumVar(0, solver.infinity(), 'y_1')
y_2 = solver.NumVar(0, solver.infinity(), 'y_2')
y_3 = solver.NumVar(0, solver.infinity(), 'y_3')

# Objective Function
solver.Minimize(F)

# Constraints
# 1. Year 2003 (Start): F = 100 + x_A + x_B + y_1
solver.Add(F - x_A - x_B - y_1 == 100)

# 2. Year 2004 (Start): 1.04*y_1 = 150 + x_C + y_2
solver.Add(1.04 * y_1 - x_C - y_2 == 150)

# 3. Year 2005 (Start): 1.25*x_B + 1.04*y_2 = 120 + y_3
solver.Add(1.25 * x_B + 1.04 * y_2 - y_3 == 120)

# 4. Year 2006 (Start): 1.40*x_A + 1.30*x_C + 1.04*y_3 = 110
solver.Add(1.40 * x_A + 1.30 * x_C + 1.04 * y_3 == 110)

# 5. Investment Limits
solver.Add(x_A <= U_A)
solver.Add(x_B <= U_B)
solver.Add(x_C <= U_C)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")