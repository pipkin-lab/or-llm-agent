import numpy as np
from scipy.optimize import minimize

# Parameters
d = {1: 100, 2: 110, 3: 120}
h = 1
s0 = 0
s3 = 0

# Variables: x1, x2, x3, s1, s2, s3
# Indices:   0   1   2   3   4   5

def objective(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x1**2 + x2**2 + x3**2 + h * (s1 + s2 + s3)

def objective_grad(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return [2 * x1, 2 * x2, 2 * x3, h, h, h]

# Equality constraints
# 1. s1 - x1 = -100
# 2. s2 - s1 - x2 = -110
# 3. s3 - s2 - x3 = -120
# 4. s3 = 0

def eq_constraint(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return [
        s1 - x1 - (-100),
        s2 - s1 - x2 - (-110),
        s3 - s2 - x3 - (-120),
        s3 - 0
    ]

def eq_jacobian(vars):
    # Rows correspond to each equality constraint
    # Cols: x1, x2, x3, s1, s2, s3
    return np.array([
        [-1,  0,  0,  1,  0,  0],
        [ 0, -1,  0, -1,  1,  0],
        [ 0,  0, -1,  0, -1,  1],
        [ 0,  0,  0,  0,  0,  1]
    ])

constraints = [
    {'type': 'eq', 'fun': eq_constraint, 'jac': eq_jacobian}
]

bounds = [
    (0, None),  # x1
    (0, None),  # x2
    (0, None),  # x3
    (0, None),  # s1
    (0, None),  # s2
    (0, None)   # s3
]

x0 = [100, 110, 120, 0, 0, 0]

result = minimize(objective, x0, jac=objective_grad, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    print("OPTIMAL_VALUE:", result.fun)
else:
    print("NO_FEASIBLE_SOLUTION")