from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Decision variables
x_M = solver.NumVar(0, inf, 'x_M')
x_B = solver.NumVar(0, inf, 'x_B')
x_E = solver.NumVar(0, inf, 'x_E')

# Deviation variables for vitamins
d_A_minus = solver.NumVar(0, inf, 'd_A_minus')
d_A_plus = solver.NumVar(0, inf, 'd_A_plus')
d_C_minus = solver.NumVar(0, inf, 'd_C_minus')
d_C_plus = solver.NumVar(0, inf, 'd_C_plus')
d_D_minus = solver.NumVar(0, inf, 'd_D_minus')
d_D_plus = solver.NumVar(0, inf, 'd_D_plus')

# Deviation variables for cholesterol and cost
d_chol_plus = solver.NumVar(0, inf, 'd_chol_plus')
d_cost_plus = solver.NumVar(0, inf, 'd_cost_plus')

# Constraints
# Vitamin A: 1*x_M + 1*x_B + 10*x_E + d_A_minus - d_A_plus = 1
solver.Add(x_M + x_B + 10 * x_E + d_A_minus - d_A_plus == 1)

# Vitamin C: 100*x_M + 10*x_B + 10*x_E + d_C_minus - d_C_plus = 30
solver.Add(100 * x_M + 10 * x_B + 10 * x_E + d_C_minus - d_C_plus == 30)

# Vitamin D: 10*x_M + 100*x_B + 10*x_E + d_D_minus - d_D_plus = 10
solver.Add(10 * x_M + 100 * x_B + 10 * x_E + d_D_minus - d_D_plus == 10)

# Cholesterol: 70*x_M + 50*x_B + 120*x_E - d_chol_plus = 0
solver.Add(70 * x_M + 50 * x_B + 120 * x_E - d_chol_plus == 0)

# Cost: 1.5*x_M + 8*x_B + 4*x_E - d_cost_plus = 0
solver.Add(1.5 * x_M + 8 * x_B + 4 * x_E - d_cost_plus == 0)

# Objective function with lexicographic priorities approximated by large weights
# P1 >> P2 >> P3
W1 = 1000000
W2 = 1000
W3 = 1

objective = W1 * (d_A_minus + d_C_minus + d_D_minus) + W2 * d_chol_plus + W3 * d_cost_plus
solver.Minimize(objective)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")