from ortools.linear_solver import pywraplp

def solve_lab_scheduling():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index sets
    S = [1, 2, 3, 4, 5, 6]
    D = [1, 2, 3, 4, 5]
    H = list(range(1, 15))  # hours 1 through 14

    # Parameters
    w = dict()
    w[1] = 10.0
    w[2] = 10.0
    w[3] = 9.9
    w[4] = 9.8
    w[5] = 10.8
    w[6] = 11.3

    # M[s][d] = maximum daily work hours
    M = dict()
    # Student 1
    M[(1, 1)] = 6
    M[(1, 2)] = 0
    M[(1, 3)] = 9
    M[(1, 4)] = 0
    M[(1, 5)] = 7
    # Student 2
    M[(2, 1)] = 0
    M[(2, 2)] = 9
    M[(2, 3)] = 0
    M[(2, 4)] = 6
    M[(2, 5)] = 0
    # Student 3
    M[(3, 1)] = 4
    M[(3, 2)] = 8
    M[(3, 3)] = 3
    M[(3, 4)] = 0
    M[(3, 5)] = 5
    # Student 4
    M[(4, 1)] = 5
    M[(4, 2)] = 5
    M[(4, 3)] = 6
    M[(4, 4)] = 0
    M[(4, 5)] = 4
    # Student 5
    M[(5, 1)] = 3
    M[(5, 2)] = 0
    M[(5, 3)] = 4
    M[(5, 4)] = 8
    M[(5, 5)] = 0
    # Student 6
    M[(6, 1)] = 0
    M[(6, 2)] = 9
    M[(6, 3)] = 0
    M[(6, 4)] = 6
    M[(6, 5)] = 3

    # L[s] = minimum weekly work hours
    L = dict()
    L[1] = 8
    L[2] = 8
    L[3] = 8
    L[4] = 8
    L[5] = 7
    L[6] = 7

    # Decision variables
    # x[s, d, h] = 1 if student s works on day d during hour h
    x = dict()
    for s in S:
        for d in D:
            for h in H:
                x[(s, d, h)] = solver.BoolVar('x_' + str(s) + '_' + str(d) + '_' + str(h))

    # y[s, d] = 1 if student s works on day d
    y = dict()
    for s in S:
        for d in D:
            y[(s, d)] = solver.BoolVar('y_' + str(s) + '_' + str(d))

    # Objective: Minimize total wage
    objective_terms = []
    for s in S:
        for d in D:
            for h in H:
                objective_terms.append(w[s] * x[(s, d, h)])
    solver.Minimize(sum(objective_terms))

    # Constraint 1: Coverage - exactly one student on duty at all times
    for d in D:
        for h in H:
            solver.Add(sum(x[(s, d, h)] for s in S) == 1)

    # Constraint 2: Maximum daily work hours
    for s in S:
        for d in D:
            solver.Add(sum(x[(s, d, h)] for h in H) <= M[(s, d)])

    # Constraint 3: Minimum weekly work hours
    for s in S:
        solver.Add(sum(x[(s, d, h)] for d in D for h in H) >= L[s])

    # Constraint 4a: Linking y and x
    for s in S:
        for d in D:
            solver.Add(sum(x[(s, d, h)] for h in H) <= 14 * y[(s, d)])

    # Constraint 4b: Maximum 2 working days per week
    for s in S:
        solver.Add(sum(y[(s, d)] for d in D) <= 2)

    # Constraint 5: Maximum 3 students per day
    for d in D:
        solver.Add(sum(y[(s, d)] for s in S) <= 3)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_lab_scheduling()