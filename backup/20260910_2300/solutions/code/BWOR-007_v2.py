from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Parameters
    C = [-12, -10, -8, -10, -4, 5, -7, -2, 15, 12, -7, 45]
    r_annual = 0.01
    r_short = 0.015
    r_dep = 0.004

    # Decision Variables
    A = solver.NumVar(0, inf, 'A')

    B = dict()
    D = dict()
    Cash = dict()

    for t in range(12):
        B[t] = solver.NumVar(0, inf, 'B_' + str(t))
        D[t] = solver.NumVar(0, inf, 'D_' + str(t))
        Cash[t] = solver.NumVar(0, inf, 'Cash_' + str(t))

    # Constraints
    # t=0 (Month 1, index 0)
    # Cash_0 = A + B_0 - D_0 + C_0
    # Note: No interest on A in month 1, no previous loans/deposits
    solver.Add(Cash[0] == A + B[0] - D[0] + C[0])

    # t=1 to 11 (Months 2 to 12, indices 1 to 11)
    for t in range(1, 12):
        # Interest on A starts from end of Feb (t=1 in 0-indexed, which is Month 2)
        # So for t >= 1 (Month 2 onwards), we subtract r_annual * A
        interest_A = r_annual * A
        
        # Cash_t = Cash_{t-1} + B_t - (1+r_short)B_{t-1} - D_t + (1+r_dep)D_{t-1} + C_t - Interest_A
        solver.Add(
            Cash[t] == Cash[t-1] + B[t] - (1 + r_short) * B[t-1] - D[t] + (1 + r_dep) * D[t-1] + C[t] - interest_A
        )

    # Objective: Maximize Cash_11 - (1 + r_short) * B_11
    # This accounts for the repayment of the last short-term loan at the beginning of the next year
    solver.Maximize(Cash[11] - (1 + r_short) * B[11])

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()