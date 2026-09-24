from ortools.linear_solver import pywraplp

def solve_grain_trading():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver")
        return

    # Parameters
    I0 = 1000
    K0 = 20000
    Ccap = 5000
    Itarget = 2000

    # Prices (index 0 corresponds to t=1, 1 to t=2, 2 to t=3)
    p = [2.85, 3.05, 2.90]  # Purchase prices
    s = [3.10, 3.25, 2.95]  # Selling prices

    # Decision Variables
    # x[t] = purchase in month t (t=0,1,2)
    # y[t] = sale in month t
    # I[t] = inventory at end of month t
    x = [None] * 3
    y = [None] * 3
    I = [None] * 3

    for t in range(3):
        x[t] = solver.NumVar(0, solver.infinity(), f'x_{t+1}')
        y[t] = solver.NumVar(0, solver.infinity(), f'y_{t+1}')
        I[t] = solver.NumVar(0, solver.infinity(), f'I_{t+1}')

    # Objective: Maximize total revenue - total cost
    objective = 0
    for t in range(3):
        objective += s[t] * y[t] - p[t] * x[t]
    solver.Maximize(objective)

    # Inventory Balance Constraints
    # I_1 = I_0 + x_1 - y_1
    solver.Add(I[0] == I0 + x[0] - y[0])
    # I_2 = I_1 + x_2 - y_2
    solver.Add(I[1] == I[0] + x[1] - y[1])
    # I_3 = I_2 + x_3 - y_3
    solver.Add(I[2] == I[1] + x[2] - y[2])

    # Sales Availability (Timing) Constraints
    # y_1 <= I_0 (only initial inventory available for month 1 sales)
    solver.Add(y[0] <= I0)
    # y_2 <= I_1 (inventory at end of month 1 available for month 2 sales)
    solver.Add(y[1] <= I[0])
    # y_3 <= I_2 (inventory at end of month 2 available for month 3 sales)
    solver.Add(y[2] <= I[1])

    # Warehouse Capacity Constraints
    for t in range(3):
        solver.Add(I[t] <= Ccap)

    # Cash Flow Constraints (Cumulative)
    # End of Month 1: p_1*x_1 - s_1*y_1 <= K_0
    solver.Add(p[0] * x[0] - s[0] * y[0] <= K0)
    # End of Month 2: p_1*x_1 + p_2*x_2 - (s_1*y_1 + s_2*y_2) <= K_0
    solver.Add(p[0] * x[0] + p[1] * x[1] - (s[0] * y[0] + s[1] * y[1]) <= K0)
    # End of Month 3: p_1*x_1 + p_2*x_2 + p_3*x_3 - (s_1*y_1 + s_2*y_2 + s_3*y_3) <= K_0
    solver.Add(p[0] * x[0] + p[1] * x[1] + p[2] * x[2] - (s[0] * y[0] + s[1] * y[1] + s[2] * y[2]) <= K0)

    # Target Inventory Constraint
    solver.Add(I[2] == Itarget)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == "__main__":
    solve_grain_trading()