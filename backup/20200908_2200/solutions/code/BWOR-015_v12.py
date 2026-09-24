from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Sets
    products = [1, 2, 3]
    stages = [1, 2, 3]

    # Parameters
    demand = dict()
    demand[1, 1] = 500
    demand[1, 2] = 680
    demand[1, 3] = 800
    demand[2, 1] = 750
    demand[2, 2] = 800
    demand[2, 3] = 950
    demand[3, 1] = 900
    demand[3, 2] = 800
    demand[3, 3] = 1000

    hours_per_unit = dict()
    hours_per_unit[1] = 2.0
    hours_per_unit[2] = 1.0
    hours_per_unit[3] = 3.1

    capital_per_unit = dict()
    capital_per_unit[1] = 40
    capital_per_unit[2] = 20
    capital_per_unit[3] = 55

    hours_limit = 5000
    capital_limit = 93000

    stockout_weights = dict()
    stockout_weights[1] = 1
    stockout_weights[2] = 1
    stockout_weights[3] = 2

    # Variables
    x = dict()
    I = dict()
    u = dict()
    vp = dict()
    vm = dict()
    cp = dict()
    cm = dict()

    for p in products:
        for t in stages:
            x[p, t] = solver.NumVar(0, inf, 'x_' + str(p) + '_' + str(t))
            u[p, t] = solver.NumVar(0, inf, 'u_' + str(p) + '_' + str(t))
            if t < 3:
                I[p, t] = solver.NumVar(0, inf, 'I_' + str(p) + '_' + str(t))
            else:
                # I[p, 3] is fixed to 0, so we don't strictly need a variable,
                # but for consistent indexing in balance equations, we can treat it as a constant 0
                # or create a variable and fix it. Let's just use 0 in the equation.
                pass

    for t in stages:
        vp[t] = solver.NumVar(0, inf, 'vp_' + str(t))
        vm[t] = solver.NumVar(0, inf, 'vm_' + str(t))
        cp[t] = solver.NumVar(0, inf, 'cp_' + str(t))
        cm[t] = solver.NumVar(0, inf, 'cm_' + str(t))

    # Constraints

    # A. Inventory Balance
    # I[p, t-1] + x[p, t] + u[p, t] = D[p, t] + I[p, t]
    # I[p, 0] = 0
    # I[p, 3] = 0
    
    for p in products:
        for t in stages:
            begin_inv = 0
            if t > 1:
                begin_inv = I[p, t - 1]
            
            end_inv = 0
            if t < 3:
                end_inv = I[p, t]
            
            solver.Add(begin_inv + x[p, t] + u[p, t] == demand[p, t] + end_inv)

    # B. Equipment Capacity (Goal Programming Form)
    # sum(a_p * x[p, t]) + vm[t] - vp[t] = H
    for t in stages:
        solver.Add(sum(hours_per_unit[p] * x[p, t] for p in products) + vm[t] - vp[t] == hours_limit)

    # C. Working Capital (Goal Programming Form)
    # sum(b_p * x[p, t]) + cm[t] - cp[t] = C
    for t in stages:
        solver.Add(sum(capital_per_unit[p] * x[p, t] for p in products) + cm[t] - cp[t] == capital_limit)

    # Preemptive Goal Programming: Lexicographic Minimization
    # Step 1: Minimize Z1 (Weighted Stockouts)
    z1_expr = sum(stockout_weights[p] * u[p, t] for p in products for t in stages)
    solver.Minimize(z1_expr)
    
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
        print("NO_FEASIBLE_SOLUTION")
        return

    z1_opt = solver.Objective().Value()
    
    # Fix Z1 to optimal value
    solver.Add(z1_expr == z1_opt)

    # Step 2: Minimize Z2 (Equipment Overloading)
    z2_expr = sum(vp[t] for t in stages)
    solver.Minimize(z2_expr)
    
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
        print("NO_FEASIBLE_SOLUTION")
        return

    z2_opt = solver.Objective().Value()
    
    # Fix Z2 to optimal value
    solver.Add(z2_expr == z2_opt)

    # Step 3: Minimize Z3 (Capital Overloading)
    z3_expr = sum(cp[t] for t in stages)
    solver.Minimize(z3_expr)
    
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        # The total objective value is typically reported as the final minimized value
        # or the sum of weighted priorities. In standard GP output, we often report the
        # final minimized term or the composite. Given the instruction to print OPTIMAL_VALUE,
        # and that this is a lexicographic problem, the "value" is often the final
        # deviation minimized. However, sometimes it's the sum of all deviations.
        # Let's print the final minimized objective (Z3) as it's the last priority.
        # But wait, usually in such problems, the "objective value" requested might be
        # the combined value or just the final status.
        # Let's look at standard practice. If P1, P2, P3 are huge weights, we'd sum them.
        # Here we did sequential. The final solver objective is Z3.
        # Let's print Z3.
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve()