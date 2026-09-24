from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Decision variables
    # x[i] = production quantity of brand i (integer, >= 0)
    # y[i] = binary indicator: 1 if brand i is produced, 0 otherwise
    x = dict()
    y = dict()
    for i in range(1, 4):
        x[i] = solver.IntVar(0, INF, 'x_' + str(i))
        y[i] = solver.BoolVar('y_' + str(i))

    # Parameters
    c = dict()
    c[1] = 2000
    c[2] = 3000
    c[3] = 4000

    a = dict()
    a[1] = 1.5
    a[2] = 3.0
    a[3] = 5.0

    b = dict()
    b[1] = 300
    b[2] = 250
    b[3] = 400

    S = 6000
    L = 600000
    M = 1000

    # Upper bounds for x_i when y_i = 1 (derived from resource constraints)
    xbar = dict()
    xbar[1] = 2000
    xbar[2] = 2000
    xbar[3] = 1200

    # Objective: maximize total profit
    objective = c[1] * x[1] + c[2] * x[2] + c[3] * x[3]
    solver.Maximize(objective)

    # Steel resource constraint
    solver.Add(a[1] * x[1] + a[2] * x[2] + a[3] * x[3] <= S)

    # Labor resource constraint
    solver.Add(b[1] * x[1] + b[2] * x[2] + b[3] * x[3] <= L)

    # Minimum batch size constraints (all-or-nothing)
    for i in range(1, 4):
        # x_i >= M * y_i
        solver.Add(x[i] >= M * y[i])
        # x_i <= xbar_i * y_i
        solver.Add(x[i] <= xbar[i] * y[i])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()