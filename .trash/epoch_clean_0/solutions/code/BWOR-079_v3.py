from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Parameters
    D = 7  # Days
    S = 5  # Shifts
    T = 5  # Time periods
    
    # Requirements per time period
    R = [0] * T
    R[0] = 18  # t=1 (6-10)
    R[1] = 20  # t=2 (10-14)
    R[2] = 19  # t=3 (14-18)
    R[3] = 17  # t=4 (18-22)
    R[4] = 12  # t=5 (22-6)
    
    # A[s][t] = 1 if shift s covers time period t
    # Shift 1 (2-10): covers t=1 (6-10) and t=5 (22-6, specifically 2-6)
    # Shift 2 (6-14): covers t=1 (6-10) and t=2 (10-14)
    # Shift 3 (10-18): covers t=2 (10-14) and t=3 (14-18)
    # Shift 4 (14-22): covers t=3 (14-18) and t=4 (18-22)
    # Shift 5 (18-2): covers t=4 (18-22) and t=5 (22-6, specifically 22-2)
    
    # Using 0-based indexing for s and t in code
    # s=0 -> Shift 1, s=1 -> Shift 2, etc.
    # t=0 -> Period 1, t=1 -> Period 2, etc.
    
    A = [[0] * T for _ in range(S)]
    
    # Shift 1 (index 0): covers t=1 (index 0) and t=5 (index 4)
    A[0][0] = 1
    A[0][4] = 1
    
    # Shift 2 (index 1): covers t=1 (index 0) and t=2 (index 1)
    A[1][0] = 1
    A[1][1] = 1
    
    # Shift 3 (index 2): covers t=2 (index 1) and t=3 (index 2)
    A[2][1] = 1
    A[2][2] = 1
    
    # Shift 4 (index 3): covers t=3 (index 2) and t=4 (index 3)
    A[3][2] = 1
    A[3][3] = 1
    
    # Shift 5 (index 4): covers t=4 (index 3) and t=5 (index 4)
    A[4][3] = 1
    A[4][4] = 1

    # Decision Variables
    # x[d][s]: number of nurses starting their 5-day block on day d (0-6) with initial shift s (0-4)
    x = {}
    for d in range(D):
        for s in range(S):
            x[d, s] = solver.IntVar(0, solver.infinity(), 'x_' + str(d) + '_' + str(s))

    # Objective: Minimize total nurses
    obj_terms = []
    for d in range(D):
        for s in range(S):
            obj_terms.append(x[d, s])
    solver.Minimize(sum(obj_terms))

    # Constraints: Coverage
    # For each day d (0-6) and time period t (0-4):
    # Sum of x[d', s'] * Cov(d, t, d', s') >= R[t]
    
    for d in range(D):
        for t in range(T):
            constraint_terms = []
            
            # Iterate over all possible start days d' and start shifts s'
            for dp in range(D):
                for sp in range(S):
                    # Calculate offset k = (d - dp) mod 7
                    k = (d - dp) % D
                    
                    # Nurse works if k is in {0, 1, 2, 3, 4}
                    if k <= 4:
                        # Current shift s_cur (0-indexed)
                        # s' is 0-indexed, so s'_1indexed = sp + 1
                        # s_cur_1indexed = ((sp + 1 - 1 + k) % 5) + 1 = ((sp + k) % 5) + 1
                        # s_cur_0indexed = (sp + k) % 5
                        s_cur = (sp + k) % S
                        
                        # Check if this shift covers time period t
                        if A[s_cur][t] == 1:
                            constraint_terms.append(x[dp, sp])
            
            if constraint_terms:
                solver.Add(sum(constraint_terms) >= R[t])
            else:
                # If no variables contribute, this is infeasible if R[t] > 0
                # But logically, there should always be coverage
                solver.Add(0 >= R[t])

    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()