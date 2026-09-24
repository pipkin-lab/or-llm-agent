from ortools.linear_solver import pywraplp

def solve_flow_shop():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Could not create solver")
        return

    # Parameters
    jobs = [1, 2, 3, 4, 5, 6]
    positions = [1, 2, 3, 4, 5, 6]
    
    a = {1: 30, 2: 60, 3: 60, 4: 20, 5: 80, 6: 90}
    b = {1: 70, 2: 70, 3: 50, 4: 60, 5: 30, 6: 40}
    
    # Decision Variables
    # x[j][p] = 1 if job j is at position p
    x = {}
    for j in jobs:
        for p in positions:
            x[j, p] = solver.BoolVar('x_{}_{}'.format(j, p))
    
    # C_A[p] = completion time on Machine A for job at position p
    C_A = {}
    for p in positions:
        C_A[p] = solver.NumVar(0, solver.infinity(), 'C_A_{}'.format(p))
        
    # C_B[p] = completion time on Machine B for job at position p
    C_B = {}
    for p in positions:
        C_B[p] = solver.NumVar(0, solver.infinity(), 'C_B_{}'.format(p))
        
    # T = Makespan
    T = solver.NumVar(0, solver.infinity(), 'T')
    
    # Constraints
    
    # 1. Each job assigned to exactly one position
    for j in jobs:
        solver.Add(sum(x[j, p] for p in positions) == 1)
        
    # 2. Each position has exactly one job
    for p in positions:
        solver.Add(sum(x[j, p] for j in jobs) == 1)
        
    # 3. Machine A Scheduling
    # C_A[1] = sum(a_j * x_j1)
    solver.Add(C_A[1] == sum(a[j] * x[j, 1] for j in jobs))
    
    # C_A[p] = C_A[p-1] + sum(a_j * x_jp) for p > 1
    for p in positions[1:]:
        solver.Add(C_A[p] == C_A[p-1] + sum(a[j] * x[j, p] for j in jobs))
        
    # 4. Machine B Scheduling
    # C_B[1] = C_A[1] + sum(b_j * x_j1)
    solver.Add(C_B[1] == C_A[1] + sum(b[j] * x[j, 1] for j in jobs))
    
    # C_B[p] >= C_B[p-1] + sum(b_j * x_jp) for p > 1
    # C_B[p] >= C_A[p] + sum(b_j * x_jp) for p > 1
    for p in positions[1:]:
        solver.Add(C_B[p] >= C_B[p-1] + sum(b[j] * x[j, p] for j in jobs))
        solver.Add(C_B[p] >= C_A[p] + sum(b[j] * x[j, p] for j in jobs))
        
    # 5. Objective Linking
    solver.Add(T >= C_B[6])
    
    # Objective
    solver.Minimize(T)
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_flow_shop()