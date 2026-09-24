from ortools.linear_solver import pywraplp

def main():
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("Could not create solver")
        return

    # Parameters
    C_cap = 5000
    I_0 = 1000
    K_0 = 20000
    I_target = 2000

    P_b = {1: 2.85, 2: 3.05, 3: 2.90}
    P_s = {1: 3.10, 2: 3.25, 3: 2.95}

    # Decision Variables
    # x_t: purchase in month t
    # y_t: sale in month t
    # I_t: inventory at end of month t
    # K_t: cash at end of month t
    x = {}
    y = {}
    I = {}
    K = {}

    for t in range(1, 4):
        x[t] = solver.NumVar(0, solver.infinity(), f'x_{t}')
        y[t] = solver.NumVar(0, solver.infinity(), f'y_{t}')
        I[t] = solver.NumVar(0, solver.infinity(), f'I_{t}')
        K[t] = solver.NumVar(0, solver.infinity(), f'K_{t}')

    # Objective: Maximize K_3
    solver.Maximize(K[3])

    # Inventory Balance Constraints
    # Month 1: I_1 = I_0 + x_1 - y_1
    solver.Add(I[1] == I_0 + x[1] - y[1])
    # Month 2: I_2 = I_1 + x_2 - y_2
    solver.Add(I[2] == I[1] + x[2] - y[2])
    # Month 3: I_3 = I_2 + x_3 - y_3
    solver.Add(I[3] == I[2] + x[3] - y[3])

    # Cash Flow Constraints
    # Month 1: K_1 = K_0 + P_s_1 * y_1 - P_b_1 * x_1
    solver.Add(K[1] == K_0 + P_s[1] * y[1] - P_b[1] * x[1])
    # Month 2: K_2 = K_1 + P_s_2 * y_2 - P_b_2 * x_2
    solver.Add(K[2] == K[1] + P_s[2] * y[2] - P_b[2] * x[2])
    # Month 3: K_3 = K_2 + P_s_3 * y_3 - P_b_3 * x_3
    solver.Add(K[3] == K[2] + P_s[3] * y[3] - P_b[3] * x[3])

    # Storage Capacity Constraints
    for t in range(1, 4):
        solver.Add(I[t] <= C_cap)

    # Sales Feasibility Constraints (Lagged Sales)
    # Month 1: y_1 <= I_0
    solver.Add(y[1] <= I_0)
    # Month 2: y_2 <= I_1
    solver.Add(y[2] <= I[1])
    # Month 3: y_3 <= I_2
    solver.Add(y[3] <= I[2])

    # Target Inventory Constraint
    solver.Add(I[3] == I_target)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == "__main__":
    main()