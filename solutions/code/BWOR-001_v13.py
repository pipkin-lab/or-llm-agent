from ortools.linear_solver import pywraplp

def solve_candy_lp():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    brands = ['X', 'Y', 'Z']
    materials = ['A', 'B', 'C']

    # Decision variables: x[i][j]
    x = dict()
    for i in brands:
        x[i] = dict()
        for j in materials:
            x[i][j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

    # Parameters
    c = dict()
    c['A'] = 2.00
    c['B'] = 1.50
    c['C'] = 1.00

    U = dict()
    U['A'] = 2000
    U['B'] = 2500
    U['C'] = 1200

    p = dict()
    p['X'] = 0.50
    p['Y'] = 0.40
    p['Z'] = 0.30

    s = dict()
    s['X'] = 3.40
    s['Y'] = 2.85
    s['Z'] = 2.25

    # Objective function: maximize profit
    obj = 0
    for i in brands:
        for j in materials:
            coeff = s[i] - p[i] - c[j]
            obj += coeff * x[i][j]

    solver.Maximize(obj)

    # Raw material availability constraints
    for j in materials:
        solver.Add(sum(x[i][j] for i in brands) <= U[j])

    # Composition constraints
    # Brand X: A >= 60% of total X => 0.4*x_XA - 0.6*x_XB - 0.6*x_XC >= 0
    solver.Add(0.4 * x['X']['A'] - 0.6 * x['X']['B'] - 0.6 * x['X']['C'] >= 0)

    # Brand Y: A >= 30% of total Y => 0.7*x_YA - 0.3*x_YB - 0.3*x_YC >= 0
    solver.Add(0.7 * x['Y']['A'] - 0.3 * x['Y']['B'] - 0.3 * x['Y']['C'] >= 0)

    # Brand Y: C <= 50% of total Y => -0.5*x_YA - 0.5*x_YB + 0.5*x_YC <= 0
    solver.Add(-0.5 * x['Y']['A'] - 0.5 * x['Y']['B'] + 0.5 * x['Y']['C'] <= 0)

    # Brand Z: C <= 60% of total Z => -0.6*x_ZA - 0.6*x_ZB + 0.4*x_ZC <= 0
    solver.Add(-0.6 * x['Z']['A'] - 0.6 * x['Z']['B'] + 0.4 * x['Z']['C'] <= 0)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_candy_lp()