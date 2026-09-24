from ortools.linear_solver import pywraplp

# Model: Goal Programming (LP) - Preemptive (Lexicographic)
# We implement lexicographic optimization by solving sequentially:
# Step 1: Minimize P1 (blending deviations)
# Step 2: Fix P1 to optimal, Minimize -Profit (Maximize Profit)
# Step 3: Fix P1 and Profit to optimal, Minimize P3 (Red shortfall)

def solve_goal_programming():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        raise RuntimeError("GLOP solver not available")

    inf = solver.infinity()

    # Sets
    grades = ['I', 'II', 'III']
    brands = ['Red', 'Yellow', 'Blue']

    # Parameters
    supply = dict()
    supply['I'] = 1500
    supply['II'] = 2000
    supply['III'] = 1000

    cost = dict()
    cost['I'] = 6.0
    cost['II'] = 4.5
    cost['III'] = 3.0

    price = dict()
    price['Red'] = 5.5
    price['Yellow'] = 5.0
    price['Blue'] = 4.8

    min_grade_I_pct = dict()
    min_grade_I_pct['Red'] = 0.50
    min_grade_I_pct['Yellow'] = 0.20
    min_grade_I_pct['Blue'] = 0.10

    max_grade_III_pct = dict()
    max_grade_III_pct['Red'] = 0.10
    max_grade_III_pct['Yellow'] = 0.70
    max_grade_III_pct['Blue'] = 0.50

    target_red = 2000

    # Decision Variables
    x = dict()
    for g in grades:
        for b in brands:
            x[g, b] = solver.NumVar(0, inf, 'x_' + g + '_' + b)

    X = dict()
    for b in brands:
        X[b] = solver.NumVar(0, inf, 'X_' + b)

    # Deviation Variables
    d_neg_I = dict()
    d_pos_I = dict()
    d_neg_III = dict()
    d_pos_III = dict()
    d_neg_red = solver.NumVar(0, inf, 'd_neg_red')
    d_pos_red = solver.NumVar(0, inf, 'd_pos_red')

    for b in brands:
        d_neg_I[b] = solver.NumVar(0, inf, 'd_neg_I_' + b)
        d_pos_I[b] = solver.NumVar(0, inf, 'd_pos_I_' + b)
        d_neg_III[b] = solver.NumVar(0, inf, 'd_neg_III_' + b)
        d_pos_III[b] = solver.NumVar(0, inf, 'd_pos_III_' + b)

    # Profit Variable
    Z = solver.NumVar(-inf, inf, 'Z')

    # Constraints

    # 1. Supply Constraints (Hard)
    for g in grades:
        expr = sum(x[g, b] for b in brands)
        solver.Add(expr <= supply[g])

    # 2. Production Balance
    for b in brands:
        expr = sum(x[g, b] for g in grades)
        solver.Add(X[b] == expr)

    # 3. Blending Goal Constraints
    for b in brands:
        # Min Grade I: x_I_b - alpha * X_b + d_pos - d_neg = 0
        expr_I = x['I', b] - min_grade_I_pct[b] * X[b] + d_pos_I[b] - d_neg_I[b]
        solver.Add(expr_I == 0)

        # Max Grade III: x_III_b - beta * X_b + d_pos - d_neg = 0
        expr_III = x['III', b] - max_grade_III_pct[b] * X[b] + d_pos_III[b] - d_neg_III[b]
        solver.Add(expr_III == 0)

    # 4. Red Production Goal
    expr_red = X['Red'] + d_pos_red - d_neg_red
    solver.Add(expr_red == target_red)

    # 5. Profit Definition
    revenue = sum(price[b] * X[b] for b in brands)
    total_cost = sum(cost[g] * sum(x[g, b] for b in brands) for g in grades)
    profit_expr = revenue - total_cost
    solver.Add(Z == profit_expr)

    # --- Lexicographic Optimization ---

    # Step 1: Minimize P1 (Blending Deviations)
    # Objective: Min sum(d_neg_I + d_pos_III)
    p1_objective = sum(d_neg_I[b] + d_pos_III[b] for b in brands)
    solver.Minimize(p1_objective)
    status = solver.Solve()
    if status not in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        print("NO_FEASIBLE_SOLUTION")
        return

    optimal_p1 = solver.Objective().Value()
    print(f"Step 1 (Min Blending Deviation): {optimal_p1}")

    # Fix P1 to optimal value
    solver.Add(p1_objective == optimal_p1)

    # Step 2: Minimize -Z (Maximize Profit)
    # Objective: Min -Z
    solver.Minimize(-Z)
    status = solver.Solve()
    if status not in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        print("NO_FEASIBLE_SOLUTION")
        return

    optimal_neg_Z = solver.Objective().Value()
    optimal_Z = -optimal_neg_Z
    print(f"Step 2 (Max Profit): {optimal_Z}")

    # Fix Profit to optimal value
    solver.Add(Z == optimal_Z)

    # Step 3: Minimize P3 (Red Shortfall)
    # Objective: Min d_neg_red
    solver.Minimize(d_neg_red)
    status = solver.Solve()
    if status not in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        print("NO_FEASIBLE_SOLUTION")
        return

    optimal_p3 = solver.Objective().Value()
    final_profit = Z.Value()
    
    # Output only the final optimal value as requested
    # The problem asks for the solution to the GP model.
    # Usually, the "result" is the vector of objectives or the primary economic value.
    # Given the instruction "output ONLY the raw numeric result", and GP has multiple objectives,
    # I will output the final Profit, as it is the primary economic metric, 
    # but strictly speaking, the GP solution is defined by the lexicographic vector.
    # However, looking at standard OR-Tools examples, if a single value is expected,
    # and the model is a blend, often the Profit is the key KPI.
    # Let's print the Profit.
    
    print("OPTIMAL_VALUE:", final_profit)

if __name__ == '__main__':
    solve_goal_programming()