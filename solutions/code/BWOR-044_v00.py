from ortools.linear_solver import pywraplp

def solve_transportation():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    origins = [1, 2, 3]
    dests = ['A', 'B', 'C']

    x = dict()
    for i in origins:
        for j in dests:
            x[i, j] = solver.NumVar(0, INF, 'x_{}_{}'.format(i, j))

    # Objective: Minimize Z = sum(c_ij * x_ij) + 5*(20 - sum_j x_1j) + 4*(40 - sum_j x_2j) + 3*(30 - sum_j x_3j)
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

    supply = dict()
    supply[1] = 20
    supply[2] = 40
    supply[3] = 30

    storage_cost = dict()
    storage_cost[1] = 5
    storage_cost[2] = 4
    storage_cost[3] = 3

    obj = 0
    for i in origins:
        for j in dests:
            obj += c[i, j] * x[i, j]
        obj += storage_cost[i] * (supply[i] - sum(x[i, j] for j in dests))

    solver.Minimize(obj)

    # Demand constraints
    demand = dict()
    demand['A'] = 30
    demand['B'] = 20
    demand['C'] = 20

    for j in dests:
        solver.Add(sum(x[i, j] for i in origins) == demand[j])

    # Supply constraints (<=)
    for i in origins:
        solver.Add(sum(x[i, j] for j in dests) <= supply[i])

    # Minimum shipment constraints
    solver.Add(x[2, 'A'] + x[2, 'B'] + x[2, 'C'] >= 38)
    solver.Add(x[3, 'A'] + x[3, 'B'] + x[3, 'C'] >= 27)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_transportation()