from ortools.linear_solver import pywraplp

def solve_staffing_problem():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index sets
    students = [1, 2, 3, 4, 5, 6]
    days = [1, 2, 3, 4, 5]

    # Parameters
    w = dict()
    w[1] = 10.0
    w[2] = 10.0
    w[3] = 9.9
    w[4] = 9.8
    w[5] = 10.8
    w[6] = 11.3

    # Maximum daily work hours M[i,d]
    M = dict()
    M[1, 1] = 6
    M[1, 2] = 0
    M[1, 3] = 9
    M[1, 4] = 0
    M[1, 5] = 7
    M[2, 1] = 0
    M[2, 2] = 9
    M[2, 3] = 0
    M[2, 4] = 6
    M[2, 5] = 0
    M[3, 1] = 4
    M[3, 2] = 8
    M[3, 3] = 3
    M[3, 4] = 0
    M[3, 5] = 5
    M[4, 1] = 5
    M[4, 2] = 5
    M[4, 3] = 6
    M[4, 4] = 0
    M[4, 5] = 4
    M[5, 1] = 3
    M[5, 2] = 0
    M[5, 3] = 4
    M[5, 4] = 8
    M[5, 5] = 0
    M[6, 1] = 0
    M[6, 2] = 9
    M[6, 3] = 0
    M[6, 4] = 6
    M[6, 5] = 3

    # Decision variables
    x = dict()
    y = dict()
    for i in students:
        for d in days:
            x[i, d] = solver.NumVar(0, M[i, d], 'x_{}_{d}'.format(i).replace('_{d}', '_{}'.format(d)))
            y[i, d] = solver.BoolVar('y_{}_{d}'.format(i).replace('_{d}', '_{}'.format(d)))

    # Objective: Minimize total wage
    obj = 0
    for i in students:
        for d in days:
            obj += w[i] * x[i, d]
    solver.Minimize(obj)

    # Constraint A: Daily coverage
    for d in days:
        solver.Add(sum(x[i, d] for i in students) == 14)

    # Constraint B: Already enforced by upper bound on x[i,d]
    # (x[i,d] <= M[i,d] is inherent in the variable definition)

    # Constraint D: x[i,d] <= M[i,d] * y[i,d]
    for i in students:
        for d in days:
            if M[i, d] > 0:
                solver.Add(x[i, d] <= M[i, d] * y[i, d])
            else:
                # If M[i,d] == 0, x[i,d] is already 0 by bound, no constraint needed
                pass

    # Constraint D: Max days scheduled per week (sum of y[i,d] <= 2)
    for i in students:
        solver.Add(sum(y[i, d] for d in days) <= 2)

    # Constraint E: Max students per day
    for d in days:
        solver.Add(sum(y[i, d] for i in students) <= 3)

    # Constraint C: Weekly minimum work hours
    for i in [1, 2, 3, 4]:
        solver.Add(sum(x[i, d] for d in days) >= 8)
    for i in [5, 6]:
        solver.Add(sum(x[i, d] for d in days) >= 7)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_staffing_problem()