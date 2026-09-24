import numpy as np
from scipy.optimize import minimize

# Parameters
D = dict()
D[1] = 450
D[2] = 480
D[3] = 540
D[4] = 600

p_H = dict()
p_H[1] = 0.10
p_H[2] = 0.20
p_H[3] = 0.15
p_H[4] = 0.25

p_L = dict()
p_L[1] = 0.08
p_L[2] = 0.16
p_L[3] = 0.12
p_L[4] = 0.20

v_H = 2
v_L = 3
F_fixed = 200

S_F = 48000
S_H = 48
S_L = 32

# Fuel costs per sortie
F_H = dict()
F_L = dict()
for i in range(1, 5):
    F_H[i] = v_H * D[i] + F_fixed
    F_L[i] = v_L * D[i] + F_fixed

# Decision variables: y[i, 'H'] and y[i, 'L'] for i in 1..4
# Total 8 variables
# Order: y1H, y2H, y3H, y4H, y1L, y2L, y3L, y4L
n_vars = 8

def get_yH(idx):
    # idx 0..3 -> i=1..4
    return idx

def get_yL(idx):
    # idx 4..7 -> i=1..4
    return idx - 4

def objective(x):
    # x is array of 8 non-negative values
    # Minimize negative of Z (since scipy minimizes)
    # Z = 1 - product of (1-p_iH)^y_iH * (1-p_iL)^y_iL
    log_not_destroyed = 0.0
    for i in range(1, 5):
        yH = x[i - 1]
        yL = x[4 + (i - 1)]
        # (1 - p_H[i])^yH * (1 - p_L[i])^yL
        # Use log to avoid underflow, but for small numbers direct is fine
        term = (1 - p_H[i]) ** yH * (1 - p_L[i]) ** yL
        log_not_destroyed += np.log(term) if term > 0 else -np.inf
    # product = exp(sum of logs)
    # Z = 1 - product
    # We want to maximize Z, so minimize -Z
    if np.isneginf(log_not_destroyed):
        product = 0.0
    else:
        product = np.exp(log_not_destroyed)
    Z = 1 - product
    return -Z

# Constraints
# 1. Total Heavy bombs <= 48
# 2. Total Light bombs <= 32
# 3. Fuel <= 48000
# 4. Non-negativity (handled by bounds)

# Inequality constraints in scipy: g(x) >= 0
def constraint_heavy(x):
    return S_H - sum(x[i] for i in range(4))

def constraint_light(x):
    return S_L - sum(x[i] for i in range(4, 8))

def constraint_fuel(x):
    fuel_used = 0.0
    for i in range(1, 5):
        yH = x[i - 1]
        yL = x[4 + (i - 1)]
        fuel_used += F_H[i] * yH + F_L[i] * yL
    return S_F - fuel_used

# Bounds: all variables non-negative, upper bound set to a large number
# But since they are integers, we'll round later. For SLSQP, use continuous relaxation.
bounds = []
for i in range(8):
    bounds.append((0, 100))  # Upper bound 100 is more than enough given constraints

constraints = [
    {'type': 'ineq', 'fun': constraint_heavy},
    {'type': 'ineq', 'fun': constraint_light},
    {'type': 'ineq', 'fun': constraint_fuel}
]

# Initial guess: spread bombs evenly
x0 = np.zeros(8)
# Try a feasible starting point
# Let's put some bombs in
x0[0] = 5  # y1H
x0[1] = 5  # y2H
x0[2] = 5  # y3H
x0[3] = 5  # y4H
x0[4] = 5  # y1L
x0[5] = 5  # y2L
x0[6] = 5  # y3L
x0[7] = 5  # y4L

# Check if x0 is feasible
if constraint_heavy(x0) < 0 or constraint_light(x0) < 0 or constraint_fuel(x0) < 0:
    # Scale down if needed
    scale = 0.5
    x0 = x0 * scale

result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

# Extract solution
x_sol = result.x

# Round to nearest integer (since y must be integer)
y_int = np.round(x_sol).astype(int)

# Ensure non-negative
y_int = np.maximum(y_int, 0)

# Check if the rounded solution is feasible. If not, try a grid search or repair.
# For simplicity, let's compute the objective on the rounded solution.
# But first, let's verify feasibility of the rounded solution.
def is_feasible(y):
    if y.shape[0] != 8:
        return False
    total_H = sum(y[:4])
    total_L = sum(y[4:])
    if total_H > S_H or total_L > S_L:
        return False
    fuel = 0
    for i in range(1, 5):
        fuel += F_H[i] * y[i-1] + F_L[i] * y[4+i-1]
    if fuel > S_F:
        return False
    return True

if not is_feasible(y_int):
    # Try to repair by reducing bombs if over budget
    # Simple heuristic: reduce the bomb with highest fuel cost per unit probability gain
    # For now, just scale down proportionally and round
    # Or do a local search
    # Let's try a simple approach: if infeasible, reduce total bombs
    while not is_feasible(y_int):
        # Find the index with highest fuel cost and reduce it
        fuel_costs = np.zeros(8)
        for i in range(1, 5):
            fuel_costs[i-1] = F_H[i]
            fuel_costs[4+i-1] = F_L[i]
        # Reduce the one with highest fuel cost if it's positive
        max_idx = np.argmax(fuel_costs * y_int)
        if y_int[max_idx] > 0:
            y_int[max_idx] -= 1
        else:
            break

# Calculate the final objective value
def calc_Z(y):
    log_not_destroyed = 0.0
    for i in range(1, 5):
        yH = y[i-1]
        yL = y[4+i-1]
        term = (1 - p_H[i]) ** yH * (1 - p_L[i]) ** yL
        if term > 0:
            log_not_destroyed += np.log(term)
        else:
            return 1.0  # If any term is 0, product is 0, Z = 1
    product = np.exp(log_not_destroyed)
    return 1 - product

final_Z = calc_Z(y_int)

print("OPTIMAL_VALUE:", final_Z)