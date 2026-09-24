from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Decision variables
    x_soy = solver.NumVar(0, inf, 'x_soy')
    x_corn = solver.NumVar(0, inf, 'x_corn')
    x_wheat = solver.NumVar(0, inf, 'x_wheat')

    y_cow = solver.NumVar(0, inf, 'y_cow')
    y_chicken = solver.NumVar(0, inf, 'y_chicken')

    u_aw = solver.NumVar(0, inf, 'u_aw')
    u_ss = solver.NumVar(0, inf, 'u_ss')

    # Objective function
    objective = (175 * x_soy + 300 * x_corn + 120 * x_wheat +
                 400 * y_cow + 2 * y_chicken +
                 1.8 * u_aw + 2.1 * u_ss)
    solver.Maximize(objective)

    # Constraints
    # Land constraint
    solver.Add(x_soy + x_corn + x_wheat + 1.5 * y_cow <= 100)

    # Funds constraint
    solver.Add(400 * y_cow + 3 * y_chicken <= 15000)

    # Labor constraints (AW)
    solver.Add(20 * x_soy + 35 * x_corn + 10 * x_wheat + 100 * y_cow + 0.6 * y_chicken + u_aw == 3500)

    # Labor constraints (SS)
    solver.Add(50 * x_soy + 75 * x_corn + 40 * x_wheat + 50 * y_cow + 0.3 * y_chicken + u_ss == 4000)

    # Capacity constraints
    solver.Add(y_cow <= 32)
    solver.Add(y_chicken <= 3000)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()