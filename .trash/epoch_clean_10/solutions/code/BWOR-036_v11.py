from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Decision variables
    x = dict()
    for t in range(1, 5):
        for k in range(t, 5):
            x[t, k] = solver.NumVar(0, inf, 'x_' + str(t) + '_' + str(k))

    # Objective function
    # Profit coefficients
    # x[1,1]: 15, x[1,2]: -140, x[1,3]: -215, x[1,4]: -325
    # x[2,2]: 10, x[2,3]: -135, x[2,4]: -245
    # x[3,3]: 5, x[3,4]: -175
    # x[4,4]: 5
    obj = (15 * x[1, 1] - 140 * x[1, 2] - 215 * x[1, 3] - 325 * x[1, 4]
           + 10 * x[2, 2] - 135 * x[2, 3] - 245 * x[2, 4]
           + 5 * x[3, 3] - 175 * x[3, 4]
           + 5 * x[4, 4])

    # Demand constraints
    # Quarter 1
    solver.Add(x[1, 1] <= 100)
    # Quarter 2
    solver.Add(x[1, 2] + x[2, 2] <= 140)
    # Quarter 3
    solver.Add(x[1, 3] + x[2, 3] + x[3, 3] <= 200)
    # Quarter 4
    solver.Add(x[1, 4] + x[2, 4] + x[3, 4] + x[4, 4] <= 160)

    # Warehouse capacity constraints
    # End of Winter (stored: x[1,2], x[1,3], x[1,4])
    solver.Add(x[1, 2] + x[1, 3] + x[1, 4] <= 20)
    # End of Spring (stored: x[1,3], x[1,4], x[2,3], x[2,4])
    solver.Add(x[1, 3] + x[1, 4] + x[2, 3] + x[2, 4] <= 20)
    # End of Summer (stored: x[1,4], x[2,4], x[3,4])
    solver.Add(x[1, 4] + x[2, 4] + x[3, 4] <= 20)

    solver.Maximize(obj)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()