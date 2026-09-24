from ortools.linear_solver import pywraplp

def solve_flow_shop():
    # Data
    n = 6
    # Processing times indexed by job (1..n)
    a = {1: 30, 2: 60, 3: 60, 4: 20, 5: 80, 6: 90}
    b = {1: 70, 2: 70, 3: 50, 4: 60, 5: 30, 6: 40}
    
    # Solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Could not create solver")
        return
    
    inf = solver.infinity()
    
    # Variables
    # x[j, k]: 1 if job j is in position k
    x = dict()
    for j in range(1, n + 1):
        for k in range(1, n + 1):
            x[j, k] = solver.BoolVar('x_' + str(j) + '_' + str(k))
    
    # S_A[k], C_A[k], S_B[k], C_B[k]
    S_A = dict()
    C_A = dict()
    S_B = dict()
    C_B = dict()
    for k in range(1, n + 1):
        S_A[k] = solver.NumVar(0, inf, 'S_A_' + str(k))
        C_A[k] = solver.NumVar(0, inf, 'C_A_' + str(k))
        S_B[k] = solver.NumVar(0, inf, 'S_B_' + str(k))
        C_B[k] = solver.NumVar(0, inf, 'C_B_' + str(k))
    
    Z = solver.NumVar(0, inf, 'Z')
    
    # Constraints
    
    # 1. Job Assignment: each job in exactly one position
    for j in range(1, n + 1):
        solver.Add(sum(x[j, k] for k in range(1, n + 1)) == 1)
    
    # 2. Position Assignment: each position has exactly one job
    for k in range(1, n + 1):
        solver.Add(sum(x[j, k] for j in range(1, n + 1)) == 1)
    
    # 3. S_A[1] = 0
    solver.Add(S_A[1] == 0)
    
    # 4. Sequential Processing on A: S_A[k] = C_A[k-1]
    for k in range(2, n + 1):
        solver.Add(S_A[k] == C_A[k - 1])
    
    # 5. Completion Time on A: C_A[k] = S_A[k] + sum_j a_j * x[j, k]
    for k in range(1, n + 1):
        solver.Add(C_A[k] == S_A[k] + sum(a[j] * x[j, k] for j in range(1, n + 1)))
    
    # 6. S_B[1] = C_A[1]
    solver.Add(S_B[1] == C_A[1])
    
    # 7. Sequential Processing on B: S_B[k] >= C_B[k-1]
    for k in range(2, n + 1):
        solver.Add(S_B[k] >= C_B[k - 1])
    
    # 8. Precedence: S_B[k] >= C_A[k]
    for k in range(1, n + 1):
        solver.Add(S_B[k] >= C_A[k])
    
    # 9. Completion Time on B: C_B[k] = S_B[k] + sum_j b_j * x[j, k]
    for k in range(1, n + 1):
        solver.Add(C_B[k] == S_B[k] + sum(b[j] * x[j, k] for j in range(1, n + 1)))
    
    # 10. Makespan: Z >= C_B[n]
    solver.Add(Z >= C_B[n])
    
    # Objective: Minimize Z
    solver.Minimize(Z)
    
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_flow_shop()