from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
# Material consumption (kg per thousand boxes)
a_A_1 = 1
a_A_2 = 2
a_B_1 = 2
a_B_2 = 1

# Material supply (kg)
S_A = 6000
S_B = 8000

# Revenue (thousand yuan per thousand boxes)
R_1 = 30
R_2 = 20

# Market constraints
U_2 = 2
D_diff = 1

# Decision variables
x_1 = solver.NumVar(0, solver.infinity(), 'x_1')
x_2 = solver.NumVar(0, solver.infinity(), 'x_2')

# Constraints

# 1. Raw Material A Availability
solver.Add(a_A_1 * x_1 + a_A_2 * x_2 <= S_A)

# 2. Raw Material B Availability
solver.Add(a_B_1 * x_1 + a_B_2 * x_2 <= S_B)

# 3. Market Constraint for Product II
solver.Add(x_2 <= U_2)

# 4. Relative Sales Constraint
solver.Add(x_2 - x_1 <= D_diff)

# Objective Function
solver.Maximize(R_1 * x_1 + R_2 * x_2)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")