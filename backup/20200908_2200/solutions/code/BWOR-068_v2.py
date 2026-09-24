from ortools.linear_solver import pywraplp

def solve_inventory_model():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print("No solver available")
        return

    # Parameters
    T = range(1, 7)  # Months 1-6
    K = range(1, 6)  # Order options 1-5

    D = {1: 40, 2: 20, 3: 30, 4: 40, 5: 30, 6: 20}
    Q = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
    C = {1: 48, 2: 86, 3: 118, 4: 138, 5: 160}
    F = 10
    h = 0.2
    H_max = 40
    I_0 = 0

    # Decision Variables
    # x[t][k] = 1 if order option k is chosen in month t
    x = {}
    for t in T:
        for k in K:
            x[t, k] = solver.BoolVar('x_{}_{}'.format(t, k))

    # I[t] = inventory at end of month t
    I = {}
    for t in T:
        I[t] = solver.IntVar(0, H_max, 'I_{}'.format(t))

    # Objective Function: Minimize total cost
    objective_terms = []
    for t in T:
        # Variable ordering costs
        for k in K:
            objective_terms.append(C[k] * x[t, k])
        # Fixed ordering cost (applied if any order is placed)
        order_indicator = sum(x[t, k] for k in K)
        objective_terms.append(F * order_indicator)
        # Holding cost
        objective_terms.append(h * I[t])

    solver.Minimize(sum(objective_terms))

    # Constraints

    # 1. Order Quantity Exclusivity: at most one order option per month
    for t in T:
        solver.Add(sum(x[t, k] for k in K) <= 1)

    # 2. Inventory Balance
    for t in T:
        if t == 1:
            prev_inv = I_0
        else:
            prev_inv = I[t - 1]
        incoming = sum(Q[k] * x[t, k] for k in K)
        solver.Add(I[t] == prev_inv + incoming - D[t])

    # 3. Inventory Capacity (already enforced by variable bounds, but explicit for clarity)
    for t in T:
        solver.Add(I[t] <= H_max)

    # 4. Non-negativity of Inventory (already enforced by variable bounds)

    # 5. End-of-Season Inventory must be zero
    solver.Add(I[6] == 0)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_inventory_model()