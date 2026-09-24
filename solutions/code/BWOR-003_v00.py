from ortools.linear_solver import pywraplp

def solve_hongyin_loan_funding():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    # Decision variables
    F = solver.NumVar(0, INF, 'F')
    xA = solver.NumVar(0, 60, 'x_A_2003')
    xB = solver.NumVar(0, 90, 'x_B_2003')
    xC = solver.NumVar(0, 50, 'x_C_2004')
    y2003 = solver.NumVar(0, INF, 'y_2003')
    y2004 = solver.NumVar(0, INF, 'y_2004')
    y2005 = solver.NumVar(0, INF, 'y_2005')
    y2006 = solver.NumVar(0, INF, 'y_2006')

    # Constraint A: Year 2003 Balance
    solver.Add(F == 100 + xA + xB + y2003)

    # Constraint B: Year 2004 Balance
    solver.Add(1.04 * y2003 == 150 + xC + y2004)

    # Constraint C: Year 2005 Balance
    solver.Add(1.04 * y2004 + 1.25 * xB == 120 + y2005)

    # Constraint D: Year 2006 Balance
    solver.Add(1.04 * y2005 + 1.30 * xC == 110 + y2006)

    # Objective: Minimize F
    solver.Minimize(F)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_hongyin_loan_funding()