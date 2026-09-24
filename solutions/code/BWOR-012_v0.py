from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    G = [1, 2, 3]
    B = ['R', 'Y', 'B']

    S = dict()
    S[1] = 1500
    S[2] = 2000
    S[3] = 1000

    C = dict()
    C[1] = 6.0
    C[2] = 4.5
    C[3] = 3.0

    P = dict()
    P['R'] = 5.5
    P['Y'] = 5.0
    P['B'] = 4.8

    MinQty_R = 2000

    x = dict()
    for g in G:
        for b in B:
            x[g, b] = solver.NumVar(0, INF, 'x_' + str(g) + '_' + b)

    # Objective: Maximize total profit
    obj = 0
    for b in B:
        for g in G:
            obj += (P[b] - C[g]) * x[g, b]
    solver.Maximize(obj)

    # Supply constraints
    for g in G:
        solver.Add(sum(x[g, b] for b in B) <= S[g])

    # Blending constraints
    # Red: Grade I >= 50%
    solver.Add(x[1, 'R'] >= 0.50 * (x[1, 'R'] + x[2, 'R'] + x[3, 'R']))
    # Red: Grade III <= 10%
    solver.Add(x[3, 'R'] <= 0.10 * (x[1, 'R'] + x[2, 'R'] + x[3, 'R']))

    # Yellow: Grade I >= 20%
    solver.Add(x[1, 'Y'] >= 0.20 * (x[1, 'Y'] + x[2, 'Y'] + x[3, 'Y']))
    # Yellow: Grade III <= 70%
    solver.Add(x[3, 'Y'] <= 0.70 * (x[1, 'Y'] + x[2, 'Y'] + x[3, 'Y']))

    # Blue: Grade I >= 10%
    solver.Add(x[1, 'B'] >= 0.10 * (x[1, 'B'] + x[2, 'B'] + x[3, 'B']))
    # Blue: Grade III <= 50%
    solver.Add(x[3, 'B'] <= 0.50 * (x[1, 'B'] + x[2, 'B'] + x[3, 'B']))

    # Minimum production constraint for Red
    solver.Add(x[1, 'R'] + x[2, 'R'] + x[3, 'R'] >= MinQty_R)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()