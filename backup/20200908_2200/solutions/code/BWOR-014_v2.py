from ortools.linear_solver import pywraplp

def solve_dietary_goal_programming():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Failed to create solver")
        return

    inf = solver.infinity()

    # Decision variables x_f for f in {1, 2, 3}
    x = {}
    for f in range(1, 4):
        x[f] = solver.NumVar(0, inf, 'x_' + str(f))

    # Deviation variables for vitamins (v in {1, 2, 3})
    d_minus = {}
    d_plus = {}
    for v in range(1, 4):
        d_minus[v] = solver.NumVar(0, inf, 'd_minus_v' + str(v))
        d_plus[v] = solver.NumVar(0, inf, 'd_plus_v' + str(v))

    # Deviation variables for cholesterol
    d_c_minus = solver.NumVar(0, inf, 'd_c_minus')
    d_c_plus = solver.NumVar(0, inf, 'd_c_plus')

    # Deviation variables for cost
    d_cost_minus = solver.NumVar(0, inf, 'd_cost_minus')
    d_cost_plus = solver.NumVar(0, inf, 'd_cost_plus')

    # Parameters
    # a[v][f]: vitamin v content in food f
    a = {
        1: {1: 1, 2: 1, 3: 10},   # Vitamin A
        2: {1: 100, 2: 10, 3: 10}, # Vitamin C
        3: {1: 10, 2: 100, 3: 10}  # Vitamin D
    }
    b = {1: 1, 2: 30, 3: 10}  # Minimum requirements
    c = {1: 70, 2: 50, 3: 120}  # Cholesterol
    p = {1: 1.5, 2: 8, 3: 4}    # Cost

    # Constraints
    # Vitamin constraints: sum_f a[v][f] * x[f] + d_minus[v] - d_plus[v] = b[v]
    for v in range(1, 4):
        expr = sum(a[v][f] * x[f] for f in range(1, 4)) + d_minus[v] - d_plus[v]
        solver.Add(expr == b[v], 'vitamin_constraint_v' + str(v))

    # Cholesterol constraint: sum_f c[f] * x[f] + d_c_minus - d_c_plus = 0
    chol_expr = sum(c[f] * x[f] for f in range(1, 4)) + d_c_minus - d_c_plus
    solver.Add(chol_expr == 0, 'cholesterol_constraint')

    # Cost constraint: sum_f p[f] * x[f] + d_cost_minus - d_cost_plus = 0
    cost_expr = sum(p[f] * x[f] for f in range(1, 4)) + d_cost_minus - d_cost_plus
    solver.Add(cost_expr == 0, 'cost_constraint')

    # Lexicographic objective:
    # Priority 1: minimize sum of d_minus[v] for v in {1,2,3}
    # Priority 2: minimize d_c_plus
    # Priority 3: minimize d_cost_plus

    # Since pywraplp does not natively support lexicographic optimization in a single call,
    # we implement it by solving sequentially with constraints added from previous objectives.

    # Step 1: Minimize Z1 = d_minus[1] + d_minus[2] + d_minus[3]
    obj1 = d_minus[1] + d_minus[2] + d_minus[3]
    solver.Minimize(obj1)
    status = solver.Solve()
    if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        print("NO_FEASIBLE_SOLUTION")
        return

    z1_val = solver.Objective().Value()
    # Fix the value of Z1 by adding a constraint
    solver.Add(d_minus[1] + d_minus[2] + d_minus[3] <= z1_val + 1e-6, 'fix_z1')

    # Step 2: Minimize Z2 = d_c_plus
    obj2 = d_c_plus
    solver.Minimize(obj2)
    status = solver.Solve()
    if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        print("NO_FEASIBLE_SOLUTION")
        return

    z2_val = solver.Objective().Value()
    # Fix the value of Z2
    solver.Add(d_c_plus <= z2_val + 1e-6, 'fix_z2')

    # Step 3: Minimize Z3 = d_cost_plus
    obj3 = d_cost_plus
    solver.Minimize(obj3)
    status = solver.Solve()
    if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        print("NO_FEASIBLE_SOLUTION")
        return

    z3_val = solver.Objective().Value()

    # Output results
    print("OPTIMAL_VALUE:", z3_val)
    print("x_1 (Milk):", x[1].solution_value())
    print("x_2 (Beef):", x[2].solution_value())
    print("x_3 (Eggs):", x[3].solution_value())
    print("Z1 (Vitamin underachievement):", z1_val)
    print("Z2 (Cholesterol):", z2_val)
    print("Z3 (Cost):", z3_val)

if __name__ == '__main__':
    solve_dietary_goal_programming()