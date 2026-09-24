import numpy as np
from scipy.optimize import minimize

# Parameters
d = {1: 100, 2: 110, 3: 120}
h = 1

# Decision variables: x1, x2, x3, s1, s2, s3
# Index: 0->x1, 1->x2, 2->x3, 3->s1, 4->s2, 5->s3

# Objective: x1^2 + x2^2 + x3^2 + s1 + s2 + s3
def objective(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x1**2 + x2**2 + x3**2 + h * (s1 + s2 + s3)

# Equality constraints (inventory balance)
# x1 - s1 = 100  =>  x1 - s1 - 100 = 0
# x2 - s2 + s1 = 110  =>  x2 - s2 + s1 - 110 = 0
# x3 - s2 = 120  =>  x3 - s2 - 120 = 0  (since s3=0)

def eq1(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x1 - s1 - d[1]

def eq2(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x2 - s2 + s1 - d[2]

def eq3(vars):
    x1, x2, x3, s1, s2, s3 = vars
    return x3 - s2 - d[3]

# Bounds: all variables >= 0
bounds = [(0, None)] * 6

# Initial guess
x0 = [100.0, 110.0, 120.0, 0.0, 0.0, 0.0]

constraints = [
    {'type': 'eq', 'fun': eq1},
    {'type': 'eq', 'fun': eq2},
    {'type': 'eq', 'fun': eq3}
]

result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)

if result.success:
    print("OPTIMAL_VALUE:", result.fun)
else:
    print("NO_FEASIBLE_SOLUTION")