from ortools.linear_solver import pywraplp

def solve_workshop_relocation():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Sets
    I = ['A', 'B', 'C', 'D', 'E']
    J = ['U', 'alpha', 'beta']
    P = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('B', 'D'), ('C', 'D'), ('D', 'E')]

    # Parameters
    # Transport volumes (tons)
    C = {
        ('A', 'B'): 1000,
        ('A', 'C'): 1500,
        ('B', 'C'): 1400,
        ('B', 'D'): 1200,
        ('C', 'D'): 2000,
        ('D', 'E'): 700
    }

    # Transport costs (yuan/ton) - assuming symmetric based on typical problems, 
    # but we define a full 3x3 matrix. The prompt implies specific values from Table C-20.
    # Since exact values for all pairs aren't explicitly listed in the text description beyond 
    # the example "500 yuan/t", I will use placeholder values that are consistent with 
    # typical distance matrices or assume a standard structure if not provided.
    # However, looking closely at the prompt, it says "From Table C-20" but doesn't list the full table.
    # It gives an example: D_{alpha,alpha} = 500? No, it says "D_{alpha alpha}=5,000 (wait, 500 yuan/t / 10,000 = 0.05)".
    # Actually, the prompt is a bit ambiguous on the exact D values. 
    # Let's look for standard values or infer. 
    # Re-reading: "D_{jl}: Transportation cost (yuan/ton)... From Table C-20".
    # Since the table is not fully provided in the text, I must make a reasonable assumption or use 
    # variables that can be easily updated. 
    # Wait, the prompt *is* the model definition. It implies the values exist. 
    # In similar textbook problems (e.g., from Operations Research textbooks), the distance/cost matrix is often:
    # Urban to Urban: 0
    # Urban to Alpha: 2
    # Urban to Beta: 3
    # Alpha to Alpha: 0
    # Alpha to Beta: 4
    # Beta to Beta: 0
    # (Values in some unit). 
    # Let's assume the following cost matrix in yuan/ton for the sake of a runnable model, 
    # as the specific numbers are missing from the prompt's data section. 
    # I will use a standard symmetric matrix often found in such examples:
    #   U  A  B
    # U  0  2  3
    # A  2  0  4
    # B  3  4  0
    # If these are incorrect, the user can update the `D` dictionary.
    D = {
        ('U', 'U'): 0, ('U', 'alpha'): 2, ('U', 'beta'): 3,
        ('alpha', 'U'): 2, ('alpha', 'alpha'): 0, ('alpha', 'beta'): 4,
        ('beta', 'U'): 3, ('beta', 'alpha'): 4, ('beta', 'beta'): 0
    }

    # Savings (yuan)
    S_alpha = {
        'A': 1000000, 'B': 1500000, 'C': 1000000, 'D': 2000000, 'E': 500000
    }
    S_beta = {
        'A': 1000000, 'B': 2000000, 'C': 1500000, 'D': 1500000, 'E': 1500000
    }

    # Variables
    # x[i][j] = 1 if workshop i is at location j
    x = {}
    for i in I:
        for j in J:
            x[i, j] = solver.BoolVar(f'x_{i}_{j}')

    # w[i][k][j][l] = 1 if workshop i is at j AND workshop k is at l, for pair (i,k) in P
    w = {}
    for (i, k) in P:
        for j in J:
            for l in J:
                w[i, k, j, l] = solver.BoolVar(f'w_{i}_{k}_{j}_{l}')

    # Objective Function
    # Minimize Total Transport Cost - Total Savings
    # Transport Cost = sum over pairs (i,k) in P of C[i][k] * sum over j,l of D[j][l] * w[i,k,j,l]
    # Savings = sum over i in I of (S_alpha[i] * x[i, 'alpha'] + S_beta[i] * x[i, 'beta'])
    
    obj_terms = []
    
    # Transport Costs
    for (i, k) in P:
        for j in J:
            for l in J:
                obj_terms.append(C[(i, k)] * D[(j, l)] * w[i, k, j, l])
    
    # Savings (subtracted from cost, so added as negative in minimization)
    for i in I:
        obj_terms.append(-S_alpha[i] * x[i, 'alpha'])
        obj_terms.append(-S_beta[i] * x[i, 'beta'])
    
    solver.Minimize(sum(obj_terms))

    # Constraints
    
    # 1. Location Assignment: Each workshop assigned to exactly one location
    for i in I:
        solver.Add(sum(x[i, j] for j in J) == 1)
    
    # 2. Capacity Constraints: Max 3 workshops per location
    for j in J:
        solver.Add(sum(x[i, j] for i in I) <= 3)
    
    # 3. Linking Constraints for w variables
    for (i, k) in P:
        # w[i,k,j,l] <= x[i,j]
        for j in J:
            for l in J:
                solver.Add(w[i, k, j, l] <= x[i, j])
                
        # w[i,k,j,l] <= x[k,l]
        for l in J:
            for j in J:
                solver.Add(w[i, k, j, l] <= x[k, l])
                
        # Sum of w[i,k,j,l] over all j,l = 1
        solver.Add(sum(w[i, k, j, l] for j in J for l in J) == 1)

    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
        # Print solution details
        print("\nSolution Details:")
        for i in I:
            for j in J:
                if x[i, j].solution_value() > 0.5:
                    print(f"Workshop {i} -> Location {j}")
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve_workshop_relocation()