from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Parameters
    C = [0, 25, 35, 30, 20]  # 1-indexed
    D = [0, 15, 20, 25, 20]  # 1-indexed
    c = [0, 12.0, 11.0, 11.5, 12.5]
    h = 0.1

    # Variables x[t, k] for 1 <= t <= k <= 4
    x = dict()
    for t in range(1, 5):
        for k in range(t, 5):
            x[t, k] = solver.NumVar(0, inf, 'x_' + str(t) + '_' + str(k))

    # Objective: Minimize total cost
    obj = 0.0
    for t in range(1, 5):
        for k in range(t, 5):
            obj += (c[t] + h * (k - t)) * x[t, k]
    solver.Minimize(obj)

    # Production capacity constraints
    for t in range(1, 5):
        prod_sum = 0.0
        for k in range(t, 5):
            prod_sum += x[t, k]
        solver.Add(prod_sum <= C[t])

    # Delivery demand constraints
    for k in range(1, 5):
        deliv_sum = 0.0
        for t in range(1, k + 1):
            deliv_sum += x[t, k]
        solver.Add(deliv_sum == D[k])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()