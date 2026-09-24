from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()

    # Index sets
    P = ['A', 'B', 'C']
    K = [0, 1, 2, 3, 4]

    # Benefits
    B = dict()
    B['A'] = [0, 41, 48, 60, 66]
    B['B'] = [0, 42, 50, 60, 66]
    B['C'] = [0, 64, 68, 78, 76]

    C_total = 4

    # Decision variables
    x = dict()
    for p in P:
        for k in K:
            x[p, k] = solver.BoolVar('x_' + str(p) + '_' + str(k))

    # Objective function
    obj = 0
    for p in P:
        for k in K:
            obj += B[p][k] * x[p, k]

    solver.Maximize(obj)

    # Constraint 1: Capital budget
    budget_expr = 0
    for p in P:
        for k in K:
            budget_expr += k * x[p, k]
    solver.Add(budget_expr <= C_total)

    # Constraint 2: Single investment level per project
    for p in P:
        level_expr = 0
        for k in K:
            level_expr += x[p, k]
        solver.Add(level_expr == 1)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()