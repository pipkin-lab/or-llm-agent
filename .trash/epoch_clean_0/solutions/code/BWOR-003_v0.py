from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Parameters
    D = {2003: 100, 2004: 150, 2005: 120, 2006: 110}
    U_A = 60
    U_B = 90
    U_C = 50
    R_A = 1.40
    R_B = 1.25
    R_C = 1.30
    R_bank = 1.04

    # Decision Variables
    C = solver.NumVar(0, inf, 'C')
    x_A = solver.NumVar(0, U_A, 'x_A')
    x_B = solver.NumVar(0, U_B, 'x_B')
    x_C = solver.NumVar(0, U_C, 'x_C')
    b_2003 = solver.NumVar(0, inf, 'b_2003')
    b_2004 = solver.NumVar(0, inf, 'b_2004')
    b_2005 = solver.NumVar(0, inf, 'b_2005')
    b_2006 = solver.NumVar(0, inf, 'b_2006')

    # Constraints
    # Year 2003: C - D_2003 = x_A + x_B + b_2003
    solver.Add(C - D[2003] == x_A + x_B + b_2003)

    # Year 2004: R_bank * b_2003 - D_2004 = x_C + b_2004
    solver.Add(R_bank * b_2003 - D[2004] == x_C + b_2004)

    # Year 2005: R_B * x_B + R_bank * b_2004 - D_2005 = b_2005
    solver.Add(R_B * x_B + R_bank * b_2004 - D[2005] == b_2005)

    # Year 2006: R_A * x_A + R_C * x_C + R_bank * b_2005 - D_2006 = b_2006
    solver.Add(R_A * x_A + R_C * x_C + R_bank * b_2005 - D[2006] == b_2006)

    # Objective: Minimize C
    solver.Minimize(C)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()