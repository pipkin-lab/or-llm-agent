from ortools.linear_solver import pywraplp

def solve_flow_shop():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Jobs indexed 1..6
    jobs = [1, 2, 3, 4, 5, 6]
    N = 6

    # Processing times
    A = dict()
    B = dict()
    A[1] = 30
    A[2] = 60
    A[3] = 60
    A[4] = 20
    A[5] = 80
    A[6] = 90

    B[1] = 70
    B[2] = 70
    B[3] = 50
    B[4] = 60
    B[5] = 30
    B[6] = 40

    M = 660

    # Decision variables
    C_A = dict()
    C_B = dict()
    for j in jobs:
        C_A[j] = solver.NumVar(0, INF, 'CA_' + str(j))
        C_B[j] = solver.NumVar(0, INF, 'CB_' + str(j))

    C_max = solver.NumVar(0, INF, 'Cmax')

    # z[i,j]: 1 if job i precedes job j (i comes before j)
    # Defined for all ordered pairs i != j
    z = dict()
    for i in jobs:
        for j in jobs:
            if i != j:
                z[i, j] = solver.BoolVar('z_' + str(i) + '_' + str(j))

    # Constraint: z[i,j] + z[j,i] == 1 for all i != j
    for i in jobs:
        for j in jobs:
            if i != j and i < j:
                solver.Add(z[i, j] + z[j, i] == 1)

    # Precedence on Machine A:
    # C_A[j] >= C_A[i] + A[j] - M*(1 - z[i,j])  for all i != j
    # Also C_A[j] >= A[j] (handled by lower bound 0 and the constraint when i precedes j)
    # Actually, we need C_A[j] >= A[j] for all j to ensure the first job on A takes A[j] time
    for j in jobs:
        solver.Add(C_A[j] >= A[j])

    for i in jobs:
        for j in jobs:
            if i != j:
                solver.Add(C_A[j] >= C_A[i] + A[j] - M * (1 - z[i, j]))

    # Precedence on Machine B:
    # C_B[j] >= C_B[i] + B[j] - M*(1 - z[i,j])  for all i != j
    # C_B[j] >= C_A[j]  (job must finish on A before starting on B)
    # C_B[j] >= B[j]
    for j in jobs:
        solver.Add(C_B[j] >= B[j])
        solver.Add(C_B[j] >= C_A[j])

    for i in jobs:
        for j in jobs:
            if i != j:
                solver.Add(C_B[j] >= C_B[i] + B[j] - M * (1 - z[i, j]))

    # Makespan definition
    for j in jobs:
        solver.Add(C_max >= C_B[j])

    # Objective: Minimize C_max
    solver.Minimize(C_max)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_flow_shop()