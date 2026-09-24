from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Define all variables
x_XY = solver.NumVar(0, INF, 'x_XY')
x_YX = solver.NumVar(0, INF, 'x_YX')
x_XA = solver.NumVar(0, INF, 'x_XA')
x_XB = solver.NumVar(0, INF, 'x_XB')
x_XC = solver.NumVar(0, INF, 'x_XC')
x_YA = solver.NumVar(0, INF, 'x_YA')
x_YB = solver.NumVar(0, INF, 'x_YB')
x_YC = solver.NumVar(0, INF, 'x_YC')
x_AB = solver.NumVar(0, INF, 'x_AB')
x_AC = solver.NumVar(0, INF, 'x_AC')
x_BA = solver.NumVar(0, INF, 'x_BA')
x_BC = solver.NumVar(0, INF, 'x_BC')
x_CA = solver.NumVar(0, INF, 'x_CA')
x_CB = solver.NumVar(0, INF, 'x_CB')

# Objective function
obj = (10 * x_XA + 14 * x_XB + 12 * x_XC +
       15 * x_YA + 12 * x_YB + 18 * x_YC +
       12 * x_XY + 10 * x_YX +
       14 * x_AB + 11 * x_AC + 10 * x_BA + 4 * x_BC + 8 * x_CA + 12 * x_CB)
solver.Minimize(obj)

# Node balance constraints
# Node X: outflow - inflow = supply
solver.Add(x_XY + x_XA + x_XB + x_XC - x_YX == 70)

# Node Y: outflow - inflow = supply
solver.Add(x_YX + x_YA + x_YB + x_YC - x_XY == 55)

# Node A: inflow - outflow = demand
solver.Add(x_XA + x_YA + x_BA + x_CA - x_AB - x_AC == 35)

# Node B: inflow - outflow = demand
solver.Add(x_XB + x_YB + x_AB + x_CB - x_BA - x_BC == 40)

# Node C: inflow - outflow = demand
solver.Add(x_XC + x_YC + x_AC + x_BC - x_CA - x_CB == 50)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")