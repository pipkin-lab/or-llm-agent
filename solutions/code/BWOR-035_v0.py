import numpy as np
from scipy.optimize import minimize

# Parameters
D = {1: 450, 2: 480, 3: 540, 4: 600}
R_H = 2
R_L = 3
R_E = 4
F_TL = 100
C_Fuel = 48000
C_H = 48
C_L = 32

P_H = {1: 0.10, 2: 0.20, 3: 0.15, 4: 0.25}
P_L = {1: 0.08, 2: 0.16, 3: 0.12, 4: 0.20}

# Fuel cost per bomb for each target
C_H_i = {i: F_TL + D[i] * (1 / R_H + 1 / R_E) for i in D}
C_L_i = {i: F_TL + D[i] * (1 / R_L + 1 / R_E) for i in D}

# Variables: x_H[0..3] for targets 1..4, x_L[0..3] for targets 1..4
# Total 8 variables
targets = [1, 2, 3, 4]
n = len(targets)
total_vars = 2 * n  # 4 heavy + 4 light

# Objective: Minimize P_all_survive = prod_i [(1-P_H_i)^x_Hi * (1-P_L_i)^x_Li]
# Since we want to MAXIMIZE Z = 1 - P_all_survive, we MINIMIZE P_all_survive.
# Note: (1-P)^x for integer x >= 0. For continuous optimization, we use exp(x * ln(1-P)).

def objective(x):
    # x[0:4] are x_H for targets 1-4
    # x[4:8] are x_L for targets 1-4
    log_survive = 0.0
    for idx in range(n):
        i = targets[idx]
        xh = x[idx]
        xl = x[n + idx]
        # Handle x=0 case: (1-P)^0 = 1, ln(1)=0
        # For numerical stability, use exp form
        if xh > 1e-10:
            log_survive += xh * np.log(1 - P_H[i])
        if xl > 1e-10:
            log_survive += xl * np.log(1 - P_L[i])
    # P_all_survive = exp(log_survive)
    # We want to minimize this.
    # If log_survive is very negative, exp is close to 0.
    return np.exp(log_survive)

# Constraints
# 1. Fuel: sum(C_H_i * x_Hi + C_L_i * x_Li) <= C_Fuel
# 2. Heavy bombs: sum(x_Hi) <= C_H
# 3. Light bombs: sum(x_Li) <= C_L
# 4. Non-negativity: x >= 0 (handled by bounds)

def constraint_fuel(x):
    fuel_used = 0.0
    for idx in range(n):
        i = targets[idx]
        fuel_used += C_H_i[i] * x[idx] + C_L_i[i] * x[n + idx]
    return C_Fuel - fuel_used  # >= 0

def constraint_heavy(x):
    return C_H - sum(x[idx] for idx in range(n))  # >= 0

def constraint_light(x):
    return C_L - sum(x[n + idx] for idx in range(n))  # >= 0

constraints = [
    {'type': 'ineq', 'fun': constraint_fuel},
    {'type': 'ineq', 'fun': constraint_heavy},
    {'type': 'ineq', 'fun': constraint_light}
]

# Bounds: x >= 0
bounds = [(0, None)] * total_vars

# Initial guess: distribute bombs evenly
x0 = np.zeros(total_vars)
x0[:n] = C_H / n
x0[n:] = C_L / n

result = minimize(
    objective,
    x0,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints,
    options={'maxiter': 1000, 'ftol': 1e-12}
)

if result.success:
    p_survive_min = result.fun
    max_prob_destroy_at_least_one = 1 - p_survive_min
    print("OPTIMAL_VALUE:", max_prob_destroy_at_least_one)
else:
    print("NO_FEASIBLE_SOLUTION")