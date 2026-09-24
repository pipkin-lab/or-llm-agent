import numpy as np
from scipy.optimize import minimize

# Parameters
# Objective: max Z = 8*x1 - x1^2 + 10*x2 - 2*x2^2
# Equivalent to: min -Z = -8*x1 + x1^2 - 10*x2 + 2*x2^2

def objective(v):
    x1, x2 = v
    return -8*x1 + x1**2 - 10*x2 + 2*x2**2

# Constraints: x1 + x2 = 5
constraints = [
    {'type': 'eq', 'fun': lambda v: v[0] + v[1] - 5}
]

# Bounds: x1 >= 0, x2 >= 0
bounds = [(0, None), (0, None)]

# Initial guess
x0 = np.array([2.5, 2.5])

result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    optimal_value = -result.fun
    print("OPTIMAL_VALUE:", optimal_value)
else:
    print("NO_FEASIBLE_SOLUTION")