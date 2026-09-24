from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Parameters
    T = 6
    D = [3000, 3600, 4000, 4600, 4800, 5000]
    p = 240
    c_mat = 150
    h_hold = 10
    w_skill = 2000
    w_train = 800
    H_worker = 160
    h_unit = 4
    H_train = 50
    r = 0.02
    I_0 = 400
    I_end_max = 100
    W_0 = 80

    # Variables
    W = dict()
    N = dict()
    P = dict()
    I = dict()

    for t in range(T):
        W[t] = solver.NumVar(0, inf, 'W_' + str(t))
        N[t] = solver.NumVar(0, inf, 'N_' + str(t))
        P[t] = solver.NumVar(0, inf, 'P_' + str(t))
        I[t] = solver.NumVar(0, inf, 'I_' + str(t))

    # Constraints
    # 1. Workforce Dynamics
    # W_1 = 80 (index 0)
    solver.Add(W[0] == W_0)
    # W_t = 0.98 * W_{t-1} + N_{t-1} for t = 1..5 (index 1..5)
    for t in range(1, T):
        solver.Add(W[t] == (1 - r) * W[t - 1] + N[t - 1])

    # 2. Production Capacity
    # 4 * P_t + 50 * N_t <= 160 * W_t
    for t in range(T):
        solver.Add(h_unit * P[t] + H_train * N[t] <= H_worker * W[t])

    # 3. Inventory Balance
    # I_t = I_{t-1} + P_t - D_t
    for t in range(T):
        if t == 0:
            solver.Add(I[t] == I_0 + P[t] - D[t])
        else:
            solver.Add(I[t] == I[t - 1] + P[t] - D[t])

    # 4. Inventory Bounds
    # I_6 <= 100 (index 5)
    solver.Add(I[T - 1] <= I_end_max)

    # Objective
    # Maximize Z = sum(90 * P_t) - 10 * sum(I_t for t=1..5) - 2000 * sum(W_t) - 800 * sum(N_t)
    # Note: Holding cost is applied to I_1..I_5 (indices 0..4). I_6 (index 5) is not held into next month.
    
    obj_expr = 0
    for t in range(T):
        obj_expr += (p - c_mat) * P[t]
    
    # Subtract holding costs for I_0 to I_4 (end of months 1 to 5)
    for t in range(T - 1):
        obj_expr -= h_hold * I[t]
    
    # Subtract labor costs
    for t in range(T):
        obj_expr -= w_skill * W[t]
        obj_expr -= w_train * N[t]

    solver.Maximize(obj_expr)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()