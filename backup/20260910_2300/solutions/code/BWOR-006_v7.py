from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    raise ValueError("Failed to create solver")

# Define variables for valid (machine, product) pairs
x_A1_I = solver.NumVar(0, solver.infinity(), 'x_A1_I')
x_A1_II = solver.NumVar(0, solver.infinity(), 'x_A1_II')

x_A2_I = solver.NumVar(0, solver.infinity(), 'x_A2_I')
x_A2_II = solver.NumVar(0, solver.infinity(), 'x_A2_II')
x_A2_III = solver.NumVar(0, solver.infinity(), 'x_A2_III')

x_B1_I = solver.NumVar(0, solver.infinity(), 'x_B1_I')
x_B1_II = solver.NumVar(0, solver.infinity(), 'x_B1_II')

x_B2_I = solver.NumVar(0, solver.infinity(), 'x_B2_I')
x_B2_III = solver.NumVar(0, solver.infinity(), 'x_B2_III')

x_B3_I = solver.NumVar(0, solver.infinity(), 'x_B3_I')

# Objective function coefficients (as derived in the model)
obj = (0.75 * x_A1_I + 0.79 * x_A2_I + 1.15 * x_A1_II + 1.38 * x_A2_II + 1.94 * x_A2_III
       - 0.36 * x_B1_I - 0.44 * x_B2_I - 0.35 * x_B3_I - 0.48 * x_B1_II - 1.21 * x_B2_III)
solver.Maximize(obj)

# Flow balance constraints
solver.Add(x_A1_I + x_A2_I == x_B1_I + x_B2_I + x_B3_I)  # Product I
solver.Add(x_A1_II + x_A2_II == x_B1_II)                  # Product II
solver.Add(x_A2_III == x_B2_III)                           # Product III

# Machine capacity constraints
solver.Add(5 * x_A1_I + 10 * x_A1_II <= 6000)    # Machine A1
solver.Add(7 * x_A2_I + 9 * x_A2_II + 12 * x_A2_III <= 10000)  # Machine A2
solver.Add(6 * x_B1_I + 8 * x_B1_II <= 4000)     # Machine B1
solver.Add(4 * x_B2_I + 11 * x_B2_III <= 7000)   # Machine B2
solver.Add(7 * x_B3_I <= 4000)                    # Machine B3

# Solve and output
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")