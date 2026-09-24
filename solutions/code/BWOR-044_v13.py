from ortools.linear_solver import pywraplp

def solve_transportation_lp():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    origins = [1, 2, 3]
    destinations = ['A', 'B', 'C']

    # Parameters
    c = dict()
    c[1, 'A'] = 1
    c[1, 'B'] = 2
    c[1, 'C'] = 2
    c[2, 'A'] = 1
    c[2, 'B'] = 4
    c[2, 'C'] = 5
    c[3, 'A'] = 2
    c[3, 'B'] = 3
    c[3, 'C'] = 3

    h = dict()
    h[1] = 5
    h[2] = 4
    h[3] = 3

    S = dict()
    S[1] = 20
    S[2] = 40
    S[3] = 30

    D = dict()
    D['A'] = 30
    D['B'] = 20
    D['C'] = 20

    # Decision variables
    x = dict()
    for i in origins:
        for j in destinations:
            x[i, j] = solver.NumVar(0, INF, 'x_%d_%s' % (i, j))

    u = dict()
    for i in origins:
        u[i] = solver.NumVar(0, INF, 'u_%d' % i)

    # Objective: minimize total cost
    obj_terms = []
    for i in origins:
        for j in destinations:
            obj_terms.append(c[i, j] * x[i, j])
        obj_terms.append(h[i] * u[i])

    objective = sum(obj_terms)
    solver.Minimize(objective)

    # Supply balance: sum_j x[i,j] + u[i] = S[i]
    for i in origins:
        supply_expr = sum(x[i, j] for j in destinations) + u[i]
        solver.Add(supply_expr == S[i])

    # Demand satisfaction: sum_i x[i,j] = D[j]
    for j in destinations:
        demand_expr = sum(x[i, j] for i in origins)
        solver.Add(demand_expr == D[j])

    # Minimum shipment constraints
    solver.Add(sum(x[2, j] for j in destinations) >= 38)
    solver.Add(sum(x[3, j] for j in destinations) >= 27)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_transportation_lp()