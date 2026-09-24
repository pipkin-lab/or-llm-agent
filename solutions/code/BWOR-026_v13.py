from ortools.linear_solver import pywraplp

def solve_two_machine_jobshop():
    # Data
    n = 12
    # Jobs 1-7: A -> B, Jobs 8-12: B -> A
    # pA[i] = processing time on Machine A
    # pB[i] = processing time on Machine B
    pA = dict()
    pB = dict()
    
    # Jobs 1-7 (A -> B)
    pA[1] = 5
    pB[1] = 5
    pA[2] = 8
    pB[2] = 9
    pA[3] = 11
    pB[3] = 4
    pA[4] = 2
    pB[4] = 3
    pA[5] = 7
    pB[5] = 7
    pA[6] = 6
    pB[6] = 9
    pA[7] = 3
    pB[7] = 5
    
    # Jobs 8-12 (B -> A)
    pA[8] = 9
    pB[8] = 4
    pA[9] = 8
    pB[9] = 9
    pA[10] = 3
    pB[10] = 5
    pA[11] = 6
    pB[11] = 3
    pA[12] = 10
    pB[12] = 4
    
    # Determine routing: 0 if A->B, 1 if B->A
    routing = dict()
    for i in range(1, n + 1):
        if i <= 7:
            routing[i] = 0  # A -> B
        else:
            routing[i] = 1  # B -> A

    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Variables
    # x[i, j] = 1 if job i is before job j in the permutation schedule
    # Defined for i < j to avoid redundancy (x[i,j] + x[j,i] == 1)
    x = dict()
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

    # Completion times on Machine A and B
    CA = dict()
    CB = dict()
    for i in range(1, n + 1):
        CA[i] = solver.NumVar(0, INF, 'CA_' + str(i))
        CB[i] = solver.NumVar(0, INF, 'CB_' + str(i))

    # Makespan
    Cmax = solver.NumVar(0, INF, 'Cmax')

    # Big M value
    # Upper bound on makespan: sum of all processing times on both machines
    # Max possible time is sum(pA) + sum(pB)
    M_BIG = sum(pA.values()) + sum(pB.values())

    # Constraints

    # 1. Routing / Precedence within a job
    for i in range(1, n + 1):
        if routing[i] == 0:  # A -> B
            solver.Add(CB[i] >= CA[i] + pB[i])
        else:  # B -> A
            solver.Add(CA[i] >= CB[i] + pA[i])

    # 2. Permutation Schedule Constraints (Sequence on Machine A and B)
    # For all i < j:
    # CA[i] + pA[i] <= CA[j] + M_BIG * (1 - x[i,j])  => CA[j] >= CA[i] + pA[i] - M_BIG * (1 - x[i,j])
    # CA[j] + pA[j] <= CA[i] + M_BIG * x[i,j]        => CA[i] >= CA[j] + pA[j] - M_BIG * x[i,j]
    # Similarly for Machine B
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            # Machine A sequencing
            solver.Add(CA[j] >= CA[i] + pA[i] - M_BIG * (1 - x[i, j]))
            solver.Add(CA[i] >= CA[j] + pA[j] - M_BIG * x[i, j])
            
            # Machine B sequencing
            solver.Add(CB[j] >= CB[i] + pB[i] - M_BIG * (1 - x[i, j]))
            solver.Add(CB[i] >= CB[j] + pB[j] - M_BIG * x[i, j])

    # 3. Makespan definition
    for i in range(1, n + 1):
        solver.Add(Cmax >= CA[i])
        solver.Add(Cmax >= CB[i])

    # Objective: Minimize Makespan
    solver.Minimize(Cmax)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_two_machine_jobshop()