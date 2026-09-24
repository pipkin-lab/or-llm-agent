from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    materials = ['A', 'B', 'C']
    brands = ['X', 'Y', 'Z']

    # Decision variables: x[i, j] = kg of material i in brand j
    x = dict()
    for i in materials:
        for j in brands:
            x[i, j] = solver.NumVar(0, inf, 'x_' + i + '_' + j)

    # Objective function coefficients
    # Max Z = 0.90 x_A_X + 1.40 x_B_X + 1.90 x_C_X
    #       + 0.45 x_A_Y + 0.95 x_B_Y + 1.45 x_C_Y
    #       - 0.05 x_A_Z + 0.45 x_B_Z + 0.95 x_C_Z

    obj = 0.0
    obj += 0.90 * x['A', 'X']
    obj += 1.40 * x['B', 'X']
    obj += 1.90 * x['C', 'X']

    obj += 0.45 * x['A', 'Y']
    obj += 0.95 * x['B', 'Y']
    obj += 1.45 * x['C', 'Y']

    obj += -0.05 * x['A', 'Z']
    obj += 0.45 * x['B', 'Z']
    obj += 0.95 * x['C', 'Z']

    solver.Maximize(obj)

    # 1. Raw Material Availability Constraints
    # Material A <= 2000
    solver.Add(x['A', 'X'] + x['A', 'Y'] + x['A', 'Z'] <= 2000)
    # Material B <= 2500
    solver.Add(x['B', 'X'] + x['B', 'Y'] + x['B', 'Z'] <= 2500)
    # Material C <= 1200
    solver.Add(x['C', 'X'] + x['C', 'Y'] + x['C', 'Z'] <= 1200)

    # 2. Composition Constraints

    # Brand X:
    # A >= 60% => 2 x_A_X - 3 x_B_X - 3 x_C_X >= 0
    solver.Add(2 * x['A', 'X'] - 3 * x['B', 'X'] - 3 * x['C', 'X'] >= 0)
    # C <= 20% => -x_A_X - x_B_X + 4 x_C_X <= 0
    solver.Add(-x['A', 'X'] - x['B', 'X'] + 4 * x['C', 'X'] <= 0)

    # Brand Y:
    # A >= 30% => 7 x_A_Y - 3 x_B_Y - 3 x_C_Y >= 0
    solver.Add(7 * x['A', 'Y'] - 3 * x['B', 'Y'] - 3 * x['C', 'Y'] >= 0)
    # C <= 50% => -x_A_Y - x_B_Y + x_C_Y <= 0
    solver.Add(-x['A', 'Y'] - x['B', 'Y'] + x['C', 'Y'] <= 0)

    # Brand Z:
    # C <= 60% => -3 x_A_Z - 3 x_B_Z + 2 x_C_Z <= 0
    solver.Add(-3 * x['A', 'Z'] - 3 * x['B', 'Z'] + 2 * x['C', 'Z'] <= 0)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()