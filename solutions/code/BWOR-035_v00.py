import math
from scipy.optimize import minimize
import numpy as np

def solve_bomber_fleet():
    # Parameters
    # p_H[i] = single heavy bomb destruction prob for part i (i=1..4)
    # p_L[i] = single light bomb destruction prob for part i
    p_H = [0.10, 0.20, 0.15, 0.25]
    p_L = [0.08, 0.16, 0.12, 0.20]
    
    # Fuel costs per bomb (liters)
    C_H = [537.5, 560.0, 605.0, 650.0]
    C_L = [462.5, 480.0, 515.0, 550.0]
    
    # Limits
    total_heavy_limit = 48
    total_light_limit = 32
    fuel_limit = 48000.0
    
    # Variables: x1, x2, x3, x4, y1, y2, y3, y4 (continuous for optimization, will round/check)
    n_vars = 8
    
    # Objective: Minimize product of Q_i (to maximize 1 - product)
    # Q_i = (1-p_H[i])^x_i * (1-p_L[i])^y_i
    # Product = prod(Q_i)
    # We minimize this product.
    
    # To handle the non-linear objective efficiently and robustly,
    # we can use the log-space or just direct minimization since values are < 1.
    # Direct minimization of the product is smooth and convex in log-space, 
    # but let's stick to the direct product for clarity, ensuring no underflow issues.
    # Since x, y are integers in the true model, but scipy minimize uses continuous,
    # we will solve the continuous relaxation and then potentially refine or accept 
    # the nearest integer solution if it's close. Given the structure, the optimum 
    # for "max probability" with independent terms often pushes resources to the 
    # most effective targets.
    
    # However, the prompt asks for OR-Tools. The objective is NON-LINEAR.
    # Rule 4: For NON-LINEAR, use scipy.optimize.minimize.
    
    # We define the variables as continuous for the scipy solver,
    # but we must ensure the final answer respects the integer nature if required by the "MILP" label in the prompt's intro,
    # BUT the objective is explicitly non-linear. The rules say:
    # "If model type is QP or NON-LINEAR... PRIMARY PATH: scipy"
    # The variables are integers in the math model. 
    # Standard approach: Solve continuous relaxation, then check integer points nearby,
    # OR use a mixed-integer non-linear solver if available (not in scipy.optimize.minimize standard interface easily).
    # Given the small search space (48x32 grid is small, but 8 vars is large),
    # let's look at the structure.
    # Actually, the most robust way for this specific "textbook" problem with scipy is to
    # recognize that the objective is monotonic. We want to MINIMIZE the product of survival probs.
    # This is equivalent to MAXIMIZING the sum of log(survival probs) with a negative sign?
    # No, minimize prod(Q_i) is equivalent to minimize sum(log(Q_i)).
    # Let f(x,y) = sum_i [ x_i * log(1-p_H[i]) + y_i * log(1-p_L[i]) ]
    # Since log(1-p) is negative, minimizing the sum of logs is maximizing the sum of absolute values?
    # Let's just minimize the product directly using SLSQP.
    
    def objective(vars):
        x1, x2, x3, x4, y1, y2, y3, y4 = vars
        # Clamp to non-negative to avoid domain issues if solver overshoots slightly
        x = [max(0, x1), max(0, x2), max(0, x3), max(0, x4)]
        y = [max(0, y1), max(0, y2), max(0, y3), max(0, y4)]
        
        q1 = (1 - p_H[0]) ** x[0] * (1 - p_L[0]) ** y[0]
        q2 = (1 - p_H[1]) ** x[1] * (1 - p_L[1]) ** y[1]
        q3 = (1 - p_H[2]) ** x[2] * (1 - p_L[2]) ** y[2]
        q4 = (1 - p_H[3]) ** x[3] * (1 - p_L[3]) ** y[3]
        
        return q1 * q2 * q3 * q4
    
    # Constraints for SLSQP: g(x) >= 0
    # 1. Heavy bomb limit: 48 - sum(xi) >= 0
    # 2. Light bomb limit: 32 - sum(yi) >= 0
    # 3. Fuel limit: 48000 - (sum C_H*xi + sum C_L*yi) >= 0
    
    def constraint_heavy(vars):
        x1, x2, x3, x4, y1, y2, y3, y4 = vars
        return total_heavy_limit - (x1 + x2 + x3 + x4)
    
    def constraint_light(vars):
        x1, x2, x3, x4, y1, y2, y3, y4 = vars
        return total_light_limit - (y1 + y2 + y3 + y4)
    
    def constraint_fuel(vars):
        x1, x2, x3, x4, y1, y2, y3, y4 = vars
        fuel_used = (C_H[0]*x1 + C_H[1]*x2 + C_H[2]*x3 + C_H[3]*x4 +
                     C_L[0]*y1 + C_L[1]*y2 + C_L[2]*y3 + C_L[3]*y4)
        return fuel_limit - fuel_used
    
    constraints = [
        {'type': 'ineq', 'fun': constraint_heavy},
        {'type': 'ineq', 'fun': constraint_light},
        {'type': 'ineq', 'fun': constraint_fuel}
    ]
    
    # Bounds: 0 to max possible (using limits as upper bounds for simplicity, though fuel is tighter)
    # Max x_i is 48, Max y_i is 32.
    bounds = [
        (0, total_heavy_limit), (0, total_heavy_limit), (0, total_heavy_limit), (0, total_heavy_limit),
        (0, total_light_limit), (0, total_light_limit), (0, total_light_limit), (0, total_light_limit)
    ]
    
    # Initial guess: distribute evenly or start with 0? 
    # Starting with 0 gives P=0. We want to maximize destruction, so we want to use resources.
    # Let's start with a feasible point that uses some resources.
    x0 = [12, 12, 12, 12, 8, 8, 8, 8] # Sum H=48, Sum L=32. Check fuel:
    # Fuel = 12*(537.5+560+605+650) + 8*(462.5+480+515+550)
    # Fuel = 12*2352.5 + 8*2007.5 = 28230 + 16060 = 44290 <= 48000. Feasible.
    
    res = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    if res.success:
        # The result is continuous. The problem asks for integers.
        # We should check the integer neighbors of the continuous solution.
        # Since the objective is smooth and the domain is small-ish, we can do a local search around the solution.
        
        # Get continuous solution
        x_cont = res.x
        
        # Define a function to check a specific integer tuple
        def calc_prob(vars_int):
            x = list(vars_int[:4])
            y = list(vars_int[4:])
            # Check feasibility
            if sum(x) > total_heavy_limit or sum(y) > total_light_limit:
                return -1 # Infeasible
            fuel = sum(C_H[i]*x[i] for i in range(4)) + sum(C_L[i]*y[i] for i in range(4))
            if fuel > fuel_limit:
                return -1 # Infeasible
            
            q1 = (1 - p_H[0]) ** x[0] * (1 - p_L[0]) ** y[0]
            q2 = (1 - p_H[1]) ** x[1] * (1 - p_L[1]) ** y[1]
            q3 = (1 - p_H[2]) ** x[2] * (1 - p_L[2]) ** y[2]
            q4 = (1 - p_H[3]) ** x[3] * (1 - p_L[3]) ** y[3]
            prod_q = q1 * q2 * q3 * q4
            return 1 - prod_q # This is the success probability we want to MAXIMIZE
        
        best_prob = -1
        best_vars = None
        
        # Search in a small neighborhood of the continuous solution
        # Rounding to nearest integer is a good start, but we need to check neighbors.
        # Since dimensions are 8, checking all 2^8 neighbors is easy.
        base = [int(round(v)) for v in x_cont]
        
        # Also check floor and ceil for each variable individually combined?
        # Better: Check all combinations of floor/ceil for each variable.
        ranges = []
        for i in range(8):
            lo = int(math.floor(x_cont[i]))
            hi = int(math.ceil(x_cont[i]))
            if lo < 0: lo = 0
            # Ensure we don't go too far from the continuous value
            candidates = [v for v in range(lo, hi+1) if v >= 0]
            if not candidates: candidates = [0]
            ranges.append(candidates)
        
        # Iterate through all combinations in this small box
        from itertools import product
        for combo in product(*ranges):
            prob = calc_prob(list(combo))
            if prob > best_prob:
                best_prob = prob
                best_vars = list(combo)
        
        # It's possible the continuous optimum is on a boundary where rounding is bad.
        # Let's also try a few random feasible integer points or a simple greedy?
        # Given the constraints, the "box" search around the continuous optimum is usually sufficient for this scale.
        # However, to be safe, let's also check the "corners" defined by the constraints?
        # Actually, the objective is concave in terms of destruction probability? 
        # 1 - prod(survival) is not necessarily concave.
        # But the problem is small. Let's do a more thorough check if the box search fails or seems low.
        # For now, the box search around the SLSQP result is the standard "hybrid" approach.
        
        # If best_vars is None, it means no feasible point was found in the box.
        if best_vars is None:
            # Fallback: try a simple feasible point
            # E.g., put all bombs on target 4 (highest prob) if fuel allows
            # But we need to respect fuel.
            # Let's just raise an error or return 0 if no feasible point found in box.
            # Given x0 was feasible, the box should contain feasible points.
            pass
        
        optimal_value = best_prob
        print("OPTIMAL_VALUE:", optimal_value)
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_bomber_fleet()