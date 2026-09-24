from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Variables
F = solver.NumVar(0, solver.infinity(), 'F')
x_A = solver.NumVar(0, solver.infinity(), 'x_A')
x_B = solver.NumVar(0, solver.infinity(), 'x_B')
x_C = solver.NumVar(0, solver.infinity(), 'x_C')
y_1 = solver.NumVar(0, solver.infinity(), 'y_1')
y_2 = solver.NumVar(0, solver.infinity(), 'y_2')
y_3 = solver.NumVar(0, solver.infinity(), 'y_3')

# Objective: Minimize F
solver.Minimize(F)

# Constraints
# 1. F - x_A - x_B - y_1 >= 100
solver.Add(F - x_A - x_B - y_1 >= 100)

# 2. 1.04*y_1 - x_C - y_2 >= 150
solver.Add(1.04 * y_1 - x_C - y_2 >= 150)

# 3. 1.04*y_2 + 1.25*x_B - y_3 >= 120
solver.Add(1.04 * y_2 + 1.25 * x_B - y_3 >= 120)

# 4. 1.04*y_3 + 1.40*x_A + 1.30*x_C >= 110
solver.Add(1.04 * y_3 + 1.40 * x_A + 1.30 * x_C >= 110)

# 5. x_A <= 60
solver.Add(x_A <= 60)

# 6. x_B <= 90
solver.Add(x_B <= 90)

# 7. x_C <= 50
solver.Add(x_C <= 50)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")