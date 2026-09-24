from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index sets
    regions = [1, 2, 3]
    K = [0, 1, 2, 3, 4]
    N = 4

    # Profit parameters
    pi = dict()
    pi[1, 0] = 0
    pi[1, 1] = 16
    pi[1, 2] = 25
    pi[1, 3] = 30
    pi[1, 4] = 32
    pi[2, 0] = 0
    pi[2, 1] = 12
    pi[2, 2] = 17
    pi[2, 3] = 21
    pi[2, 4] = 22
    pi[3, 0] = 0
    pi[3, 1] = 10
    pi[3, 2] = 14
    pi[3, 3] = 16
    pi[3, 4] = 17

    # Decision variables
    x = dict()
    for r in regions:
        for k in K:
            x[r, k] = solver.BoolVar('x_' + str(r) + '_' + str(k))

    # Objective: maximize total profit
    obj_terms = []
    for r in regions:
        for k in K:
            obj_terms.append(pi[r, k] * x[r, k])
    solver.Maximize(sum(obj_terms))

    # Constraint 1: exactly one allocation per region
    for r in regions:
        solver.Add(sum(x[r, k] for k in K) == 1)

    # Constraint 2: total outlet budget
    solver.Add(sum(k * x[r, k] for r in regions for k in K) == N)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()