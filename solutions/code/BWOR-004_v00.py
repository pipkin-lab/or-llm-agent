from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    T = list(range(1, 7))  # Months 1 through 6

    # Decision variables
    W = dict()  # Skilled workers in month t
    H = dict()  # Trainees hired in month t
    X = dict()  # Production in month t
    I = dict()  # Ending inventory in month t

    for t in T:
        W[t] = solver.IntVar(0, INF, 'W_' + str(t))
        H[t] = solver.IntVar(0, INF, 'H_' + str(t))
        X[t] = solver.IntVar(0, INF, 'X_' + str(t))
        I[t] = solver.IntVar(0, INF, 'I_' + str(t))

    # Demand
    D = dict()
    D[1] = 3000
    D[2] = 3600
    D[3] = 4000
    D[4] = 4600
    D[5] = 4800
    D[6] = 5000

    # Initial inventory
    I0 = 400

    # Workforce constraints
    # W_1 = 80
    solver.Add(W[1] == 80)

    # W_t = 0.98 * W_{t-1} + H_{t-1} for t = 2, 3, 4, 5, 6
    # Since W and H are integers, we need to handle the 0.98 coefficient.
    # 0.98 = 49/50. So 50 * W_t = 49 * W_{t-1} + 50 * H_{t-1}
    # However, pywraplp handles linear expressions with floating point coefficients directly.
    # Let's use the direct form.
    for t in range(2, 7):
        solver.Add(W[t] == 0.98 * W[t - 1] + H[t - 1])

    # Production Capacity Constraints: 4 X_t + 50 H_t <= 160 W_t
    for t in T:
        solver.Add(4 * X[t] + 50 * H[t] <= 160 * W[t])

    # Inventory Balance Constraints
    # I_t = I_{t-1} + X_t - D_t
    solver.Add(I[1] == I0 + X[1] - D[1])
    for t in range(2, 7):
        solver.Add(I[t] == I[t - 1] + X[t] - D[t])

    # Inventory constraints
    for t in T:
        solver.Add(I[t] >= 0)
    
    # I_6 <= 100
    solver.Add(I[6] <= 100)

    # Objective Function: Maximize sum(90 X_t - 2000 W_t - 800 H_t - 10 I_t)
    obj_terms = []
    for t in T:
        obj_terms.append(90 * X[t] - 2000 * W[t] - 800 * H[t] - 10 * I[t])
    
    objective = sum(obj_terms)
    solver.Maximize(objective)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()