from ortools.linear_solver import pywraplp

def solve_engine_replacement():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Parameters
    D = dict()
    D[1] = 100
    D[2] = 70
    D[3] = 80
    D[4] = 120
    D[5] = 150
    D[6] = 140

    C_new = 10
    C_fast = 2
    C_slow = 10

    # Decision Variables
    # N_t: new engines purchased in period t, t=1..6
    N = dict()
    for t in range(1, 7):
        N[t] = solver.IntVar(0, INF, 'N_' + str(t))

    # F_t: fast repair initiated in period t, t=1..5
    F = dict()
    for t in range(1, 6):
        F[t] = solver.IntVar(0, INF, 'F_' + str(t))

    # S_t: slow repair initiated in period t, t=1..4
    S = dict()
    for t in range(1, 5):
        S[t] = solver.IntVar(0, INF, 'S_' + str(t))

    # Objective: Minimize total cost
    objective = 0
    for t in range(1, 7):
        objective += C_new * N[t]
    for t in range(1, 6):
        objective += C_fast * F[t]
    for t in range(1, 5):
        objective += C_slow * S[t]

    solver.Minimize(objective)

    # Demand Satisfaction Constraints
    # Period 1: N_1 = D_1
    solver.Add(N[1] == D[1])
    # Period 2: N_2 + F_1 = D_2
    solver.Add(N[2] + F[1] == D[2])
    # Period 3: N_3 + F_2 + S_1 = D_3
    solver.Add(N[3] + F[2] + S[1] == D[3])
    # Period 4: N_4 + F_3 + S_2 = D_4
    solver.Add(N[4] + F[3] + S[2] == D[4])
    # Period 5: N_5 + F_4 + S_3 = D_5
    solver.Add(N[5] + F[4] + S[3] == D[5])
    # Period 6: N_6 + F_5 + S_4 = D_6
    solver.Add(N[6] + F[5] + S[4] == D[6])

    # Used Engine Availability Constraints (Cumulative)
    # t=1: F_1 + S_1 <= D_1
    solver.Add(F[1] + S[1] <= D[1])
    # t=2: F_1 + S_1 + F_2 + S_2 <= D_1 + D_2
    solver.Add(F[1] + S[1] + F[2] + S[2] <= D[1] + D[2])
    # t=3: F_1 + S_1 + F_2 + S_2 + F_3 + S_3 <= D_1 + D_2 + D_3
    solver.Add(F[1] + S[1] + F[2] + S[2] + F[3] + S[3] <= D[1] + D[2] + D[3])
    # t=4: F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 <= D_1 + ... + D_4
    solver.Add(F[1] + S[1] + F[2] + S[2] + F[3] + S[3] + F[4] + S[4] <= D[1] + D[2] + D[3] + D[4])
    # t=5: F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 + F_5 <= D_1 + ... + D_5
    # Note: S_5 is not defined (slow repair from 5 arrives in 7, outside horizon)
    solver.Add(F[1] + S[1] + F[2] + S[2] + F[3] + S[3] + F[4] + S[4] + F[5] <= D[1] + D[2] + D[3] + D[4] + D[5])
    # t=6: F_1 + S_1 + F_2 + S_2 + F_3 + S_3 + F_4 + S_4 + F_5 <= D_1 + ... + D_6
    # Note: No repairs sent in 6 are useful. S_5, S_6, F_6 not defined.
    solver.Add(F[1] + S[1] + F[2] + S[2] + F[3] + S[3] + F[4] + S[4] + F[5] <= D[1] + D[2] + D[3] + D[4] + D[5] + D[6])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_engine_replacement()