from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
x['XY'] = solver.NumVar(0, INF, 'x_XY')
x['YX'] = solver.NumVar(0, INF, 'x_YX')
x['XA'] = solver.NumVar(0, INF, 'x_XA')
x['XB'] = solver.NumVar(0, INF, 'x_XB')
x['XC'] = solver.NumVar(0, INF, 'x_XC')
x['YA'] = solver.NumVar(0, INF, 'x_YA')
x['YB'] = solver.NumVar(0, INF, 'x_YB')
x['YC'] = solver.NumVar(0, INF, 'x_YC')
x['AB'] = solver.NumVar(0, INF, 'x_AB')
x['AC'] = solver.NumVar(0, INF, 'x_AC')
x['BA'] = solver.NumVar(0, INF, 'x_BA')
x['BC'] = solver.NumVar(0, INF, 'x_BC')
x['CA'] = solver.NumVar(0, INF, 'x_CA')
x['CB'] = solver.NumVar(0, INF, 'x_CB')

# Objective: minimize total transport distance
solver.Minimize(
    12 * x['XY'] + 10 * x['YX'] +
    10 * x['XA'] + 14 * x['XB'] + 12 * x['XC'] +
    15 * x['YA'] + 12 * x['YB'] + 18 * x['YC'] +
    14 * x['AB'] + 11 * x['AC'] +
    10 * x['BA'] + 4 * x['BC'] +
    8 * x['CA'] + 12 * x['CB']
)

# Flow balance constraints
# Node X (supply = 70)
solver.Add(x['XY'] + x['XA'] + x['XB'] + x['XC'] - x['YX'] == 70)

# Node Y (supply = 55)
solver.Add(x['YA'] + x['YB'] + x['YC'] - x['XY'] == 55)

# Node A (demand = 35)
solver.Add(x['XA'] + x['YA'] + x['BA'] + x['CA'] - x['AB'] - x['AC'] == 35)

# Node B (demand = 40)
solver.Add(x['XB'] + x['YB'] + x['AB'] + x['CB'] - x['BA'] - x['BC'] == 40)

# Node C (demand = 50)
solver.Add(x['XC'] + x['YC'] + x['AC'] + x['BC'] - x['CA'] - x['CB'] == 50)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")