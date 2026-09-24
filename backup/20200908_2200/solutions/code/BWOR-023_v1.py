from ortools.linear_solver import pywraplp

def solve_tsp():
    # Define the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("No solver found")
        return

    # Problem data
    V = [1, 2, 3, 4]
    n = len(V)
    
    # Distance matrix c[i][j]
    # c[i][j] is distance from city i to city j
    # Cities are 1-indexed in the problem, so we use a dict or 2D list with 1-based indexing
    # Let's use a dictionary for clarity or a 5x5 matrix (indices 0-4, use 1-4)
    c = {
        (1, 2): 6, (1, 3): 7, (1, 4): 9,
        (2, 1): 8, (2, 3): 9, (2, 4): 7,
        (3, 1): 5, (3, 2): 8, (3, 4): 8,
        (4, 1): 6, (4, 2): 5, (4, 3): 5
    }
    
    # Decision Variables
    # x[i, j] = 1 if path goes from i to j
    x = {}
    for i in V:
        for j in V:
            if i != j:
                x[i, j] = solver.BoolVar(f'x_{i}_{j}')
                
    # Auxiliary variables for MTZ constraints
    # u[i] represents the position of city i in the tour
    # u[1] is fixed to 1
    u = {}
    for i in V:
        if i == 1:
            u[i] = solver.NumVar(1, n, f'u_{i}')
        else:
            u[i] = solver.NumVar(1, n, f'u_{i}')
            
    # Fix u[1] = 1
    solver.Add(u[1] == 1)
    
    # Objective Function: Minimize total distance
    objective = 0
    for i in V:
        for j in V:
            if i != j:
                objective += c[(i, j)] * x[i, j]
                
    solver.Minimize(objective)
    
    # Constraints
    
    # A. Flow Conservation
    for i in V:
        # Outgoing flow
        out_flow = sum(x[i, j] for j in V if j != i)
        solver.Add(out_flow == 1)
        
        # Incoming flow
        in_flow = sum(x[j, i] for j in V if j != i)
        solver.Add(in_flow == 1)
        
    # B. Subtour Elimination (MTZ)
    # u[i] - u[j] + n * x[i, j] <= n - 1
    # This constraint is applied for all arcs (i, j) where i != j and i != 1 and j != 1?
    # Standard MTZ: u[i] - u[j] <= n * (1 - x[i, j]) for all i, j in V\{start}
    # Or: u[i] - u[j] + n * x[i, j] <= n - 1
    # Let's stick to the provided formula: u_i - u_j + n x_{ij} <= n - 1
    # This is typically applied for i, j in {2, ..., n} to avoid issues with the start node.
    # If i=1, u[1]=1. If j=1, u[j]=1.
    # If we apply it for all i, j != 1, it works.
    # What if i=1? u[1] - u[j] + n*x[1,j] <= n-1 => 1 - u[j] + n*x[1,j] <= n-1.
    # If x[1,j]=1, 1-u[j] <= n-1 => u[j] >= 2-n, which is always true since u[j]>=1.
    # If x[1,j]=0, 1-u[j] <= n-1 => u[j] >= 2-n, true.
    # What if j=1? u[i] - u[1] + n*x[i,1] <= n-1 => u[i] - 1 + n*x[i,1] <= n-1.
    # If x[i,1]=1, u[i]-1 <= n-1 => u[i] <= n, which is the upper bound.
    # If x[i,1]=0, u[i]-1 <= n-1 => u[i] <= n, true.
    # So it is safe to apply for all i, j in V, i != j.
    
    for i in V:
        for j in V:
            if i != j:
                solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)
                
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
        # Optional: Print the path for verification
        # path = []
        # current = 1
        # while True:
        #     path.append(current)
        #     for next_city in V:
        #         if next_city != current and x[current, next_city].solution_value() > 0.5:
        #             current = next_city
        #             break
        #     if current == 1:
        #         break
        # print("PATH:", " -> ".join(map(str, path)))
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == "__main__":
    solve_tsp()