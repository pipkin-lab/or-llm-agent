from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

materials = ['A', 'B', 'C']
brands = ['X', 'Y', 'Z']

# Decision variables: x[material][brand]
x = dict()
for i in materials:
    for j in brands:
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# Objective function coefficients
# x_AX: 0.90, x_BX: 1.40, x_CX: 1.90
# x_AY: 0.45, x_BY: 0.95, x_CY: 1.45
# x_AZ: -0.05, x_BZ: 0.45, x_CZ: 0.95

objective = 0.90 * x['A', 'X'] + 1.40 * x['B', 'X'] + 1.90 * x['C', 'X']
objective += 0.45 * x['A', 'Y'] + 0.95 * x['B', 'Y'] + 1.45 * x['C', 'Y']
objective += -0.05 * x['A', 'Z'] + 0.45 * x['B', 'Z'] + 0.95 * x['C', 'Z']

solver.Maximize(objective)

# Composition Constraints
# Brand X: A >= 60% => 0.40*x_AX - 0.60*x_BX - 0.60*x_CX >= 0
solver.Add(0.40 * x['A', 'X'] - 0.60 * x['B', 'X'] - 0.60 * x['C', 'X'] >= 0)
# Brand X: C <= 20% => -0.20*x_AX - 0.20*x_BX + 0.80*x_CX <= 0
solver.Add(-0.20 * x['A', 'X'] - 0.20 * x['B', 'X'] + 0.80 * x['C', 'X'] <= 0)

# Brand Y: A >= 30% => 0.70*x_AY - 0.30*x_BY - 0.30*x_CY >= 0
solver.Add(0.70 * x['A', 'Y'] - 0.30 * x['B', 'Y'] - 0.30 * x['C', 'Y'] >= 0)
# Brand Y: C <= 50% => -0.50*x_AY - 0.50*x_BY + 0.50*x_CY <= 0
solver.Add(-0.50 * x['A', 'Y'] - 0.50 * x['B', 'Y'] + 0.50 * x['C', 'Y'] <= 0)

# Brand Z: C <= 60% => -0.60*x_AZ - 0.60*x_BZ + 0.40*x_CZ <= 0
solver.Add(-0.60 * x['A', 'Z'] - 0.60 * x['B', 'Z'] + 0.40 * x['C', 'Z'] <= 0)

# Resource Constraints
# Material A <= 2000
solver.Add(x['A', 'X'] + x['A', 'Y'] + x['A', 'Z'] <= 2000)
# Material B <= 2500
solver.Add(x['B', 'X'] + x['B', 'Y'] + x['B', 'Z'] <= 2500)
# Material C <= 1200
solver.Add(x['C', 'X'] + x['C', 'Y'] + x['C', 'Z'] <= 1200)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")