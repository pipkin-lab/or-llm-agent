from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x_1 through x_7 (binary)
x1 = solver.BoolVar('x1')  # Calculus
x2 = solver.BoolVar('x2')  # Operations Research
x3 = solver.BoolVar('x3')  # Data Structures
x4 = solver.BoolVar('x4')  # Managerial Statistics
x5 = solver.BoolVar('x5')  # Computer Simulation
x6 = solver.BoolVar('x6')  # Computer Programming
x7 = solver.BoolVar('x7')  # Forecasting

# Objective: Minimize total courses selected
solver.Minimize(x1 + x2 + x3 + x4 + x5 + x6 + x7)

# Category Constraints
# Math: exactly 2
solver.Add(x1 + x2 + x3 + x4 + x7 == 2)

# OR: exactly 2
solver.Add(x2 + x4 + x5 + x7 == 2)

# CS: exactly 2
solver.Add(x3 + x5 + x6 == 2)

# Prerequisite Constraints
# x5 <= x6
solver.Add(x5 <= x6)
# x3 <= x6
solver.Add(x3 <= x6)
# x4 <= x1
solver.Add(x4 <= x1)
# x7 <= x4
solver.Add(x7 <= x4)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")