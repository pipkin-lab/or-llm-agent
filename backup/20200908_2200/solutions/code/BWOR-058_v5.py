from ortools.linear_solver import pywraplp

def solve_mall_lease():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Could not create solver")
        return

    # Index sets
    I = [1, 2, 3, 4, 5]

    # Parameters
    area_limit = 5000
    a = {1: 250, 2: 350, 3: 800, 4: 400, 5: 500}
    L = {1: 1, 2: 1, 3: 1, 4: 0, 5: 1}
    U = {1: 3, 2: 2, 3: 3, 4: 2, 5: 3}

    # Profit per store p[i][k]
    p = {
        1: {1: 9, 2: 8, 3: 7},
        2: {1: 10, 2: 9},
        3: {1: 27, 2: 21, 3: 20},
        4: {1: 16, 2: 10},
        5: {1: 17, 2: 15, 3: 12}
    }

    # Decision variables x[i][k]
    x = {}
    for i in I:
        for k in range(L[i], U[i] + 1):
            x[i, k] = solver.BoolVar(f'x_{i}_{k}')

    # Objective function: Maximize total rent income
    obj_terms = []
    for i in I:
        for k in range(L[i], U[i] + 1):
            if k == 0:
                coeff = 0.0
            else:
                coeff = k * p[i][k] * 0.2
            obj_terms.append(coeff * x[i, k])

    solver.Maximize(solver.Sum(obj_terms))

    # Exclusivity constraints: exactly one k per category
    for i in I:
        solver.Add(solver.Sum(x[i, k] for k in range(L[i], U[i] + 1)) == 1)

    # Area constraint
    area_terms = []
    for i in I:
        for k in range(L[i], U[i] + 1):
            area_coeff = k * a[i]
            area_terms.append(area_coeff * x[i, k])

    solver.Add(solver.Sum(area_terms) <= area_limit)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve_mall_lease()