from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("No solver found")
        return

    W_max = 15
    V_max = 10

    weights = [0, 2, 3, 4, 5]
    volumes = [0, 2, 2, 2, 3]
    values = [0, 3, 4, 5, 6]

    n_items = 4
    x = dict()
    for i in range(1, n_items + 1):
        x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

    weight_expr = sum(weights[i] * x[i] for i in range(1, n_items + 1))
    volume_expr = sum(volumes[i] * x[i] for i in range(1, n_items + 1))
    obj_expr = sum(values[i] * x[i] for i in range(1, n_items + 1))

    solver.Add(weight_expr <= W_max)
    solver.Add(volume_expr <= V_max)

    solver.Maximize(obj_expr)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()