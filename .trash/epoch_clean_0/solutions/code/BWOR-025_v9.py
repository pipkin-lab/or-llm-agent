from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Job indices: 1..12
    J = list(range(1, 13))

    # Processing times
    pA = dict()
    pB = dict()
    pA[1] = 5
    pA[2] = 8
    pA[3] = 11
    pA[4] = 2
    pA[5] = 7
    pA[6] = 6
    pA[7] = 3
    pA[8] = 9
    pA[9] = 8
    pA[10] = 3
    pA[11] = 6
    pA[12] = 10

    pB[1] = 5
    pB[2] = 9
    pB[3] = 4
    pB[4] = 3
    pB[5] = 7
    pB[6] = 9
    pB[7] = 5
    pB[8] = 4
    pB[9] = 9
    pB[10] = 5
    pB[11] = 3
    pB[12] = 4

    # Big-M
    M = sum(pA.values())  # 78

    # Decision variables
    sA = dict()
    cA = dict()
    sB = dict()
    cB = dict()

    for i in J:
        sA[i] = solver.NumVar(0, inf, 'sA_' + str(i))
        cA[i] = solver.NumVar(0, inf, 'cA_' + str(i))
        sB[i] = solver.NumVar(0, inf, 'sB_' + str(i))
        cB[i] = solver.NumVar(0, inf, 'cB_' + str(i))

    T = solver.NumVar(0, inf, 'T')

    # Binary ordering variables x[i,j] for i < j
    x = dict()
    for i in J:
        for j in J:
            if i < j:
                x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

    # Completion time definitions
    for i in J:
        solver.Add(cA[i] == sA[i] + pA[i])
        solver.Add(cB[i] == sB[i] + pB[i])

    # Machine A precedence (no overlap)
    for i in J:
        for j in J:
            if i < j:
                # If x[i,j]=1 (i before j): s_j >= c_i
                # If x[i,j]=0 (j before i): s_i >= c_j
                solver.Add(sB if False else sA[j] >= cA[i] - M * (1 - x[i, j]))
                solver.Add(sA[i] >= cA[j] - M * x[i, j])

    # Machine B precedence (same order as A, no overlap)
    for i in J:
        for j in J:
            if i < j:
                solver.Add(sB[j] >= cB[i] - M * (1 - x[i, j]))
                solver.Add(sB[i] >= cB[j] - M * x[i, j])

    # Flow shop: job cannot start on B before finishing on A
    for i in J:
        solver.Add(sB[i] >= cA[i])

    # Makespan
    for i in J:
        solver.Add(T >= cB[i])

    # Objective: minimize makespan
    solver.Minimize(T)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == "__main__":
    main()