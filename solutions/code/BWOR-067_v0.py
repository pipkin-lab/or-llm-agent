import numpy as np
from scipy.optimize import minimize

# Parameters
d = [0, 100, 110, 120]  # 1-indexed: d[1], d[2], d[3]
h = 1
s0 = 0
s3_target = 0

# Decision variables: x1, x2, x3, s1, s2, s3
# Index mapping: 0->x1, 1->x2, 2->x3, 3->s1, 4->s2, 5->s3
n_vars = 6

def objective(v):
    x1, x2, x3, s1, s2, s3 = v
    return x1**2 + x2**2 + x3**2 + h * (s1 + s2 + s3)

# Equality constraints (scipy expects g(v) >= 0 for 'ineq', and h(v) == 0 for 'eq')
# We use equality constraints for inventory balances and terminal inventory.
# s1 - x1 + 100 = 0  -> s1 - x1 = -100
# s2 - s1 - x2 + 110 = 0 -> s2 - s1 - x2 = -110
# s3 - s2 - x3 + 120 = 0 -> s3 - s2 - x3 = -120
# s3 = 0

def eq_constraint_1(v):
    x1, x2, x3, s1, s2, s3 = v
    return s1 - x1 + 100

def eq_constraint_2(v):
    x1, x2, x3, s1, s2, s3 = v
    return s2 - s1 - x2 + 110

def eq_constraint_3(v):
    x1, x2, x3, s1, s2, s3 = v
    return s3 - s2 - x3 + 120

def eq_constraint_4(v):
    x1, x2, x3, s1, s2, s3 = v
    return s3

constraints = [
    {'type': 'eq', 'fun': eq_constraint_1},
    {'type': 'eq', 'fun': eq_constraint_2},
    {'type': 'eq', 'fun': eq_constraint_3},
    {'type': 'eq', 'fun': eq_constraint_4},
]

# Bounds: all variables >= 0
bounds = [(0, None)] * n_vars

# Initial guess
x0 = np.array([100, 110, 120, 0, 0, 0])

result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    print("OPTIMAL_VALUE:", result.fun)
else:
    print("NO_FEASIBLE_SOLUTION")