import numpy as np
from scipy.optimize import minimize

# Parameters
d = {1: 100, 2: 110, 3: 120}
h = 1
s0 = 0
s3 = 0

# Variable order: [x1, x2, x3, I1, I2]
# Index:            0    1    2    3    4

def objective(v):
    x1, x2, x3, I1, I2 = v
    return x1**2 + x2**2 + x3**2 + h * I1 + h * I2

def gradient(v):
    x1, x2, x3, I1, I2 = v
    return np.array([2*x1, 2*x2, 2*x3, h, h])

# Equality constraints:
# 1. I1 - x1 = -100  =>  -x1 + I1 + 100 = 0
# 2. I1 - I2 - x2 = -110  =>  -x2 + I1 - I2 + 110 = 0
# 3. I2 + x3 = 120  =>  x3 + I2 - 120 = 0

def eq1(v):
    x1, x2, x3, I1, I2 = v
    return -x1 + I1 + 100

def eq2(v):
    x1, x2, x3, I1, I2 = v
    return -x2 + I1 - I2 + 110

def eq3(v):
    x1, x2, x3, I1, I2 = v
    return x3 + I2 - 120

constraints = [
    {'type': 'eq', 'fun': eq1},
    {'type': 'eq', 'fun': eq2},
    {'type': 'eq', 'fun': eq3}
]

bounds = [
    (0, None),  # x1
    (0, None),  # x2
    (0, None),  # x3
    (0, None),  # I1
    (0, None)   # I2
]

x0 = np.array([100.0, 110.0, 120.0, 0.0, 0.0])

result = minimize(objective, x0, jac=gradient, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    print("OPTIMAL_VALUE:", result.fun)
else:
    print("NO_FEASIBLE_SOLUTION")