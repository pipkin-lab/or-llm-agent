from ortools.linear_solver import pywraplp

def solve_tsp():
    # Parameters
    n = 4
    # Distances (1-indexed, using 0-indexed in code for Python)
    # d[i][j] where i, j are 0-indexed (0 corresponds to city 1)
    d = [
        [0, 6, 7, 9],
        [8, 0, 9, 7],
        [5, 8, 0, 8],
        [6, 5, 5, 0]
    ]
    
    # Solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Variables
    # x[i, j] = 1 if path goes from i to j
    x = dict()
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))
    
    # u[i] for MTZ constraint
    u = dict()
    for i in range(n):
        u[i] = solver.NumVar(0, n - 1, 'u_' + str(i))
    
    # Constraints
    # 1. Flow conservation: Each city entered exactly once
    for j in range(n):
        solver.Add(sum(x[i, j] for i in range(n) if i != j) == 1)
        
    # 2. Flow conservation: Each city exited exactly once
    for i in range(n):
        solver.Add(sum(x[i, j] for j in range(n) if i != j) == 1)
        
    # 3. MTZ Subtour Elimination
    # u_i - u_j + n * x_ij <= n - 1
    for i in range(n):
        for j in range(n):
            if i != j:
                solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)
                
    # Fix u[0] = 0 (City 1 is start)
    solver.Add(u[0] == 0)
    
    # Objective: Minimize total distance
    obj = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                obj += d[i][j] * x[i, j]
                
    solver.Minimize(obj)
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_tsp()