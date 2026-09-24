import numpy as np
from scipy.optimize import minimize

# Demand values
d = [100, 110, 120]
n_months = 3

# Variables: x_1, x_2, x_3, s_1, s_2, s_3
# Index mapping:
# 0: x_1
# 1: x_2
# 2: x_3
# 3: s_1
# 4: s_2
# 5: s_3

def objective(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x1**2 + x2**2 + x3**2 + s1 + s2 + s3

# Equality constraints:
# s_1 = 0 + x_1 - 100  =>  x_1 - s_1 - 100 = 0
# s_2 = s_1 + x_2 - 110 => x_2 + s_1 - s_2 - 110 = 0
# s_3 = s_2 + x_3 - 120 => x_3 + s_2 - s_3 - 120 = 0
# s_3 = 0 => s_3 = 0

def eq1(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x1 - s1 - 100

def eq2(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x2 + s1 - s2 - 110

def eq3(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x3 + s2 - s3 - 120

def eq4(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return s3

constraints = [
    {'type': 'eq', 'fun': eq1},
    {'type': 'eq', 'fun': eq2},
    {'type': 'eq', 'fun': eq3},
    {'type': 'eq', 'fun': eq4},
]

# Bounds: all variables >= 0
bounds = [(0, None)] * 6

# Initial guess
x0 = np.array([100.0, 110.0, 120.0, 0.0, 0.0, 0.0])

result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    print("OPTIMAL_VALUE:", result.fun)
else:
    print("NO_FEASIBLE_SOLUTION")