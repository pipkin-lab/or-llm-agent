from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Define decision variables (all continuous, non-negative)
x_XA = solver.NumVar(0, solver.infinity(), 'x_XA')
x_XB = solver.NumVar(0, solver.infinity(), 'x_XB')
x_XC = solver.NumVar(0, solver.infinity(), 'x_XC')
x_YA = solver.NumVar(0, solver.infinity(), 'x_YA')
x_YB = solver.NumVar(0, solver.infinity(), 'x_YB')
x_YC = solver.NumVar(0, solver.infinity(), 'x_YC')
x_AB = solver.NumVar(0, solver.infinity(), 'x_AB')
x_AC = solver.NumVar(0, solver.infinity(), 'x_AC')
x_BA = solver.NumVar(0, solver.infinity(), 'x_BA')
x_BC = solver.NumVar(0, solver.infinity(), 'x_BC')
x_CA = solver.NumVar(0, solver.infinity(), 'x_CA')
x_CB = solver.NumVar(0, solver.infinity(), 'x_CB')

# Objective function: Minimize total transport distance
objective = (
    10 * x_XA + 14 * x_XB + 12 * x_XC +
    15 * x_YA + 12 * x_YB + 18 * x_YC +
    14 * x_AB + 11 * x_AC +
    10 * x_BA + 4 * x_BC +
    8 * x_CA + 12 * x_CB
)
solver.Minimize(objective)

# Supply constraints (outflow from origins)
solver.Add(x_XA + x_XB + x_XC == 70)
solver.Add(x_YA + x_YB + x_YC == 55)

# Demand/Flow conservation constraints at destinations
# Node A: inflow (from X, Y, B, C) - outflow (to B, C) = 35
solver.Add(x_XA + x_YA + x_BA + x_CA - x_AB - x_AC == 35)

# Node B: inflow (from X, Y, A, C) - outflow (to A, C) = 40
solver.Add(x_XB + x_YB + x_AB + x_CB - x_BA - x_BC == 40)

# Node C: inflow (from X, Y, A, B) - outflow (to A, B) = 50
solver.Add(x_XC + x_YC + x_AC + x_BC - x_CA - x_CB == 50)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")