from ortools.linear_solver import pywraplp

def solve_grain_trading():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("NO_FEASIBLE_SOLUTION")
        return

    INF = solver.infinity()

    # Parameters
    T = [1, 2, 3]
    I0 = 1000
    M0 = 20000
    Cmax = 5000
    I_target = 2000
    P_buy = dict()
    P_buy[1] = 2.85
    P_buy[2] = 3.05
    P_buy[3] = 2.90
    P_sell = dict()
    P_sell[1] = 3.10
    P_sell[2] = 3.25
    P_sell[3] = 2.95

    # Decision Variables
    x = dict()  # purchases
    y = dict()  # sales
    I = dict()  # inventory
    M = dict()  # cash

    for t in T:
        x[t] = solver.NumVar(0, INF, 'x_' + str(t))
        y[t] = solver.NumVar(0, INF, 'y_' + str(t))
        I[t] = solver.NumVar(0, INF, 'I_' + str(t))
        M[t] = solver.NumVar(0, INF, 'M_' + str(t))

    # Objective: Maximize profit
    obj = 0
    for t in T:
        obj += P_sell[t] * y[t] - P_buy[t] * x[t]
    solver.Maximize(obj)

    # Constraints
    for t in T:
        # Inventory balance
        if t == 1:
            solver.Add(I[t] == I0 + x[t] - y[t])
        else:
            solver.Add(I[t] == I[t - 1] + x[t] - y[t])

        # Sellability lag: sales limited by beginning-of-month inventory
        if t == 1:
            solver.Add(y[t] <= I0)
        else:
            solver.Add(y[t] <= I[t - 1])

        # Warehouse capacity
        solver.Add(I[t] <= Cmax)

        # Cash flow
        if t == 1:
            solver.Add(M[t] == M0 + P_sell[t] * y[t] - P_buy[t] * x[t])
        else:
            solver.Add(M[t] == M[t - 1] + P_sell[t] * y[t] - P_buy[t] * x[t])

    # Target inventory at end of March
    solver.Add(I[3] == I_target)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_grain_trading()