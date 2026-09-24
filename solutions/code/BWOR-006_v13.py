from ortools.linear_solver import pywraplp

def solve_production_plan():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    # Decision variables
    x_A1_I = solver.NumVar(0, INF, 'x_A1_I')
    x_A1_II = solver.NumVar(0, INF, 'x_A1_II')
    x_A2_I = solver.NumVar(0, INF, 'x_A2_I')
    x_A2_II = solver.NumVar(0, INF, 'x_A2_II')
    x_A2_III = solver.NumVar(0, INF, 'x_A2_III')
    x_B1_I = solver.NumVar(0, INF, 'x_B1_I')
    x_B1_II = solver.NumVar(0, INF, 'x_B1_II')
    x_B2_I = solver.NumVar(0, INF, 'x_B2_I')
    x_B2_III = solver.NumVar(0, INF, 'x_B2_III')
    x_B3_I = solver.NumVar(0, INF, 'x_B3_I')

    # Objective function
    objective = (0.75 * x_A1_I + 1.15 * x_A1_II + 0.79 * x_A2_I + 1.38 * x_A2_II + 1.94 * x_A2_III
                 - 0.36 * x_B1_I - 0.48 * x_B1_II - 0.44 * x_B2_I - 1.21 * x_B2_III - 0.35 * x_B3_I)
    solver.Maximize(objective)

    # Flow balance constraints
    solver.Add(x_A1_I + x_A2_I == x_B1_I + x_B2_I + x_B3_I)
    solver.Add(x_A1_II + x_A2_II == x_B1_II)
    solver.Add(x_A2_III == x_B2_III)

    # Machine capacity constraints
    solver.Add(5 * x_A1_I + 10 * x_A1_II <= 6000)
    solver.Add(7 * x_A2_I + 9 * x_A2_II + 12 * x_A2_III <= 10000)
    solver.Add(6 * x_B1_I + 8 * x_B1_II <= 4000)
    solver.Add(4 * x_B2_I + 11 * x_B2_III <= 7000)
    solver.Add(7 * x_B3_I <= 4000)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_plan()