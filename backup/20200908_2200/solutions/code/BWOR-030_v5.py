from ortools.linear_solver import pywraplp

def solve_grain_trading():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver")
        return

    infinity = solver.infinity()

    # Parameters
    C_wh = 5000
    I_0 = 1000
    K_0 = 20000
    I_target = 2000

    P_buy = {1: 2.85, 2: 3.05, 3: 2.90}
    P_sell = {1: 3.10, 2: 3.25, 3: 2.95}

    # Decision Variables
    # x[t]: quantity purchased in month t
    # s[t]: quantity sold in month t
    # I[t]: inventory at end of month t
    x = {}
    s = {}
    I = {}

    for t in [1, 2, 3]:
        x[t] = solver.NumVar(0, infinity, f'x_{t}')
        s[t] = solver.NumVar(0, infinity, f's_{t}')
        I[t] = solver.NumVar(0, infinity, f'I_{t}')

    # Objective Function: Maximize Profit
    # Z = sum(P_sell[t] * s[t]) - sum(P_buy[t] * x[t])
    obj_terms = []
    for t in [1, 2, 3]:
        obj_terms.append(P_sell[t] * s[t])
        obj_terms.append(-P_buy[t] * x[t])
    
    solver.Maximize(sum(obj_terms))

    # Constraints

    # 1. Inventory Balance
    # I_1 = I_0 + x_1 - s_1
    solver.Add(I[1] == I_0 + x[1] - s[1])
    # I_2 = I_1 + x_2 - s_2
    solver.Add(I[2] == I[1] + x[2] - s[2])
    # I_3 = I_2 + x_3 - s_3
    solver.Add(I[3] == I[2] + x[3] - s[3])

    # 2. Sales Availability (Enforcing "Next Month" Rule)
    # s_1 <= I_0
    solver.Add(s[1] <= I_0)
    # s_2 <= I_1
    solver.Add(s[2] <= I[1])
    # s_3 <= I_2
    solver.Add(s[3] <= I[2])

    # 3. Warehouse Capacity
    for t in [1, 2, 3]:
        solver.Add(I[t] <= C_wh)

    # 4. Capital Constraints (No Negative Cash)
    # C_1 >= 0 => K_0 + P_sell[1]*s[1] - P_buy[1]*x[1] >= 0
    # Rearranged: -P_sell[1]*s[1] + P_buy[1]*x[1] <= K_0
    # Or: P_buy[1]*x[1] - P_sell[1]*s[1] <= K_0
    solver.Add(P_buy[1] * x[1] - P_sell[1] * s[1] <= K_0)
    
    # C_2 >= 0 => C_1 + P_sell[2]*s[2] - P_buy[2]*x[2] >= 0
    # (K_0 + P_sell[1]*s[1] - P_buy[1]*x[1]) + P_sell[2]*s[2] - P_buy[2]*x[2] >= 0
    # -P_sell[1]*s[1] - P_sell[2]*s[2] + P_buy[1]*x[1] + P_buy[2]*x[2] <= K_0
    solver.Add(P_buy[1] * x[1] + P_buy[2] * x[2] - P_sell[1] * s[1] - P_sell[2] * s[2] <= K_0)

    # C_3 >= 0 => C_2 + P_sell[3]*s[3] - P_buy[3]*x[3] >= 0
    # (K_0 + P_sell[1]*s[1] - P_buy[1]*x[1] + P_sell[2]*s[2] - P_buy[2]*x[2]) + P_sell[3]*s[3] - P_buy[3]*x[3] >= 0
    # -P_sell[1]*s[1] - P_sell[2]*s[2] - P_sell[3]*s[3] + P_buy[1]*x[1] + P_buy[2]*x[2] + P_buy[3]*x[3] <= K_0
    solver.Add(P_buy[1] * x[1] + P_buy[2] * x[2] + P_buy[3] * x[3] - P_sell[1] * s[1] - P_sell[2] * s[2] - P_sell[3] * s[3] <= K_0)

    # 5. Target Ending Inventory
    solver.Add(I[3] == I_target)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
        print("Solution details:")
        for t in [1, 2, 3]:
            print(f"Month {t}:")
            print(f"  Purchase (x_{t}): {x[t].solution_value():.2f}")
            print(f"  Sale (s_{t}): {s[t].solution_value():.2f}")
            print(f"  End Inventory (I_{t}): {I[t].solution_value():.2f}")
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == "__main__":
    solve_grain_trading()