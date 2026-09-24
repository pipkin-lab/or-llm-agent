from ortools.linear_solver import pywraplp

def solve_investment():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("Could not create solver")
        return

    inf = solver.infinity()

    # Parameters
    F = 1000.0
    R_reserve = 100.0
    total_investable = F - R_reserve  # 900

    r_A = 0.05
    r_B = 0.07
    r_C = 0.10

    L_A = 300.0
    U_share = 0.35 * F  # 350

    # Decision variables
    x_A = solver.NumVar(0, inf, 'x_A')
    x_B = solver.NumVar(0, inf, 'x_B')
    x_C = solver.NumVar(0, inf, 'x_C')

    # Objective
    solver.Maximize(r_A * x_A + r_B * x_B + r_C * x_C)

    # Constraints
    # Total investment
    solver.Add(x_A + x_B + x_C <= total_investable)

    # Minimum for A
    solver.Add(x_A >= L_A)

    # Maximum per product
    solver.Add(x_A <= U_share)
    solver.Add(x_B <= U_share)
    solver.Add(x_C <= U_share)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve_investment()