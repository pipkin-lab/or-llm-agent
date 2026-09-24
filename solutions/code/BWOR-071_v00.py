import scipy.optimize as sco
import numpy as np

# Objective: Maximize Z = -x1^2 + 8*x1 - 2*x2^2 + 10*x2
# Equivalent to minimizing -Z = x1^2 - 8*x1 + 2*x2^2 - 10*x2

def objective(x):
    x1, x2 = x
    return x1**2 - 8*x1 + 2*x2**2 - 10*x2

# Constraint: x1 + x2 = 5
constraints = [
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 5}
]

bounds = [(0, None), (0, None)]

x0 = np.array([2.5, 2.5])

result = sco.minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    x1_val, x2_val = result.x
    z_val = -(result.fun)
    print("OPTIMAL_VALUE:", z_val)
else:
    print("NO_FEASIBLE_SOLUTION")