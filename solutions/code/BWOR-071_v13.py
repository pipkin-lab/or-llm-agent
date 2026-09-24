import numpy as np
from scipy.optimize import minimize

# Parameters
C = 5
t1 = 1
t2 = 1
c1 = 4
c2 = 3
a1 = 12
b1 = 1
a2 = 13
b2 = 2

# Objective: Maximize Z = -x1^2 - 2*x2^2 + 8*x1 + 10*x2
# Minimize -Z = x1^2 + 2*x2^2 - 8*x1 - 10*x2
def objective(x):
    x1, x2 = x
    return x1**2 + 2*x2**2 - 8*x1 - 10*x2

# Constraint: x1 + x2 = 5
def constraint_eq(x):
    x1, x2 = x
    return x1 + x2 - C

constraints = [
    {'type': 'eq', 'fun': constraint_eq}
]

# Bounds: x1 >= 0, x2 >= 0
bounds = [(0, None), (0, None)]

# Initial guess
x0 = np.array([2.5, 2.5])

result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    x1_opt, x2_opt = result.x
    z_opt = -result.fun
    print("OPTIMAL_VALUE:", z_opt)
else:
    print("NO_FEASIBLE_SOLUTION")