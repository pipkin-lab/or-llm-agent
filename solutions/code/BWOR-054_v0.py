from ortools.linear_solver import pywraplp

def solve_shift_scheduling():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index sets
    I = [1, 2, 3, 4, 5, 6]
    I_UG = [1, 2, 3, 4]
    I_GR = [5, 6]
    D = [1, 2, 3, 4, 5]

    # Parameters
    w = dict()
    w[1] = 10.0
    w[2] = 10.0
    w[3] = 9.9
    w[4] = 9.8
    w[5] = 10.8
    w[6] = 11.3

    M = dict()
    M[(1, 1)] = 6; M[(1, 2)] = 0; M[(1, 3)] = 9; M[(1, 4)] = 0; M[(1, 5)] = 7
    M[(2, 1)] = 0; M[(2, 2)] = 9; M[(2, 3)] = 0; M[(2, 4)] = 6; M[(2, 5)] = 0
    M[(3, 1)] = 4; M[(3, 2)] = 8; M[(3, 3)] = 3; M[(3, 4)] = 0; M[(3, 5)] = 5
    M[(4, 1)] = 5; M[(4, 2)] = 5; M[(4, 3)] = 6; M[(4, 4)] = 0; M[(4, 5)] = 4
    M[(5, 1)] = 3; M[(5, 2)] = 0; M[(5, 3)] = 4; M[(5, 4)] = 8; M[(5, 5)] = 0
    M[(6, 1)] = 0; M[(6, 2)] = 9; M[(6, 3)] = 0; M[(6, 4)] = 6; M[(6, 5)] = 3

    H = 15
    R_UG = 8
    R_GR = 7
    K = 2
    N_max = 3

    # Decision variables
    x = dict()
    h = dict()
    for i in I:
        for d in D:
            x[i, d] = solver.BoolVar('x_' + str(i) + '_' + str(d))
            h[i, d] = solver.NumVar(0, INF, 'h_' + str(i) + '_' + str(d))

    # Objective: minimize total wage
    obj_terms = []
    for i in I:
        for d in D:
            obj_terms.append(w[i] * h[i, d])
    solver.Minimize(sum(obj_terms))

    # Constraint 1: Daily coverage - total hours per day = 15
    for d in D:
        solver.Add(sum(h[i, d] for i in I) == H)

    # Constraint 2: Binary-Hours linking: h[i,d] <= M[i,d] * x[i,d]
    for i in I:
        for d in D:
            if M[i, d] > 0:
                solver.Add(h[i, d] <= M[i, d] * x[i, d])
            else:
                solver.Add(h[i, d] == 0)

    # Constraint 3: Max days worked per student
    for i in I:
        solver.Add(sum(x[i, d] for d in D) <= K)

    # Constraint 4: Max students on duty per day
    for d in D:
        solver.Add(sum(x[i, d] for i in I) <= N_max)

    # Constraint 5: Min weekly hours - Undergraduate
    for i in I_UG:
        solver.Add(sum(h[i, d] for d in D) >= R_UG)

    # Constraint 6: Min weekly hours - Graduate
    for i in I_GR:
        solver.Add(sum(h[i, d] for d in D) >= R_GR)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_shift_scheduling()