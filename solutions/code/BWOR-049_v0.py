from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables f_ij for each directed arc (i, j) in E
f_XY = solver.NumVar(0, INF, 'f_XY')
f_YX = solver.NumVar(0, INF, 'f_YX')
f_XA = solver.NumVar(0, INF, 'f_XA')
f_XB = solver.NumVar(0, INF, 'f_XB')
f_XC = solver.NumVar(0, INF, 'f_XC')
f_YA = solver.NumVar(0, INF, 'f_YA')
f_YB = solver.NumVar(0, INF, 'f_YB')
f_YC = solver.NumVar(0, INF, 'f_YC')
f_AB = solver.NumVar(0, INF, 'f_AB')
f_AC = solver.NumVar(0, INF, 'f_AC')
f_BA = solver.NumVar(0, INF, 'f_BA')
f_BC = solver.NumVar(0, INF, 'f_BC')
f_CA = solver.NumVar(0, INF, 'f_CA')
f_CB = solver.NumVar(0, INF, 'f_CB')

# Objective: minimize total distance
solver.Minimize(
    12 * f_XY + 10 * f_YX
    + 10 * f_XA + 14 * f_XB + 12 * f_XC
    + 15 * f_YA + 12 * f_YB + 18 * f_YC
    + 14 * f_AB + 11 * f_AC
    + 10 * f_BA + 4 * f_BC
    + 8 * f_CA + 12 * f_CB
)

# Flow conservation constraints

# Node X (origin): supply = outflow
solver.Add(f_XY + f_XA + f_XB + f_XC == 70)

# Node Y (origin): supply = outflow
solver.Add(f_YX + f_YA + f_YB + f_YC == 55)

# Node A (destination/transit): inflow = outflow + demand
solver.Add(f_XA + f_YA + f_BA + f_CA == f_AB + f_AC + 35)

# Node B (destination/transit): inflow = outflow + demand
solver.Add(f_XB + f_YB + f_AB + f_CB == f_BA + f_BC + 40)

# Node C (destination/transit): inflow = outflow + demand
solver.Add(f_XC + f_YC + f_AC + f_BC == f_CA + f_CB + 50)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")