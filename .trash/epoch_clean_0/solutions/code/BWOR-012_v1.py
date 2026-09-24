from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Index sets
    G = [1, 2, 3]
    P = ['R', 'Y', 'B']

    # Parameters
    S = {1: 1500, 2: 2000, 3: 1000}
    C = {1: 6.0, 2: 4.5, 3: 3.0}
    Price = {'R': 5.5, 'Y': 5.0, 'B': 4.8}
    MinProd = {'R': 2000, 'Y': 0, 'B': 0}

    # Decision variables
    x = dict()
    for g in G:
        for p in P:
            x[g, p] = solver.NumVar(0, inf, 'x_{}_{}'.format(g, p))

    z = dict()
    for p in P:
        z[p] = solver.NumVar(0, inf, 'z_{}'.format(p))

    # Objective function
    obj = 0
    for p in P:
        obj += Price[p] * z[p]
    for g in G:
        for p in P:
            obj -= C[g] * x[g, p]

    solver.Maximize(obj)

    # Constraints
    # 1. Production definition (Mass Balance)
    for p in P:
        solver.Add(z[p] == sum(x[g, p] for g in G))

    # 2. Minimum Production
    for p in P:
        solver.Add(z[p] >= MinProd[p])

    # 3. Supply Constraints
    for g in G:
        solver.Add(sum(x[g, p] for p in P) <= S[g])

    # 4. Blending Proportion Constraints
    # Red
    solver.Add(x[1, 'R'] >= 0.50 * z['R'])
    solver.Add(x[3, 'R'] <= 0.10 * z['R'])

    # Yellow
    solver.Add(x[1, 'Y'] >= 0.20 * z['Y'])
    solver.Add(x[3, 'Y'] <= 0.70 * z['Y'])

    # Blue
    solver.Add(x[1, 'B'] >= 0.10 * z['B'])
    solver.Add(x[3, 'B'] <= 0.50 * z['B'])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()