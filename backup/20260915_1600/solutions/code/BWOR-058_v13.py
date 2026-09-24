from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index sets and parameters
    # K_i: allowed number of stores for type i
    K = dict()
    K[1] = [1, 2, 3]
    K[2] = [1, 2]
    K[3] = [1, 2, 3]
    K[4] = [0, 1, 2]
    K[5] = [1, 2, 3]

    # Area per store
    A = dict()
    A[1] = 250
    A[2] = 350
    A[3] = 800
    A[4] = 400
    A[5] = 500

    # Profit per store when k stores are opened
    P = dict()
    P[(1, 1)] = 9
    P[(1, 2)] = 8
    P[(1, 3)] = 7
    P[(2, 1)] = 10
    P[(2, 2)] = 9
    P[(3, 1)] = 27
    P[(3, 2)] = 21
    P[(3, 3)] = 20
    P[(4, 1)] = 16
    P[(4, 2)] = 10
    P[(5, 1)] = 17
    P[(5, 2)] = 15
    P[(5, 3)] = 12

    rent_rate = 0.2
    total_area = 5000

    # Decision variables x[i, k]
    x = dict()
    for i in [1, 2, 3, 4, 5]:
        for k in K[i]:
            x[i, k] = solver.BoolVar('x_{}_{}'.format(i, k))

    # Objective: Maximize total rental income
    obj_terms = []
    for i in [1, 2, 3, 4, 5]:
        for k in K[i]:
            if k == 0:
                profit_per_store = 0
            else:
                profit_per_store = P[(i, k)]
            coeff = k * profit_per_store * rent_rate
            if coeff != 0:
                obj_terms.append(coeff * x[i, k])

    solver.Maximize(sum(obj_terms))

    # Selection constraints: exactly one configuration per store type
    for i in [1, 2, 3, 4, 5]:
        solver.Add(sum(x[i, k] for k in K[i]) == 1)

    # Area constraint
    area_terms = []
    for i in [1, 2, 3, 4, 5]:
        for k in K[i]:
            area_terms.append(A[i] * k * x[i, k])
    solver.Add(sum(area_terms) <= total_area)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()