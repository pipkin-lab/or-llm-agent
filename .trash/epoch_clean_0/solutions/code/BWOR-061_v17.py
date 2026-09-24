import numpy as np

# Quadratic Binary Programming (QBP):
# Maximize Z = 2.296 + 0.04*x2 - 0.06*x1 - 0.025*x1*x2
# Equivalent to: Minimize -Z = -2.296 - 0.04*x2 + 0.06*x1 + 0.025*x1*x2
# In standard QP form: min (1/2)*x^T Q x + c^T x
# x = [x1, x2]

# Build Q such that (1/2)*x^T Q x = 0.025*x1*x2
# x^T Q x = 2*Q[0,1]*x1*x2 + Q[0,0]*x1^2 + Q[1,1]*x2^2
# For binary vars, x^2 = x, but we use the standard form.
# We want (1/2)*x^T Q x + c^T x = 0.025*x1*x2 - 0.06*x1 - 0.04*x2
# So (1/2)*Q[0,1] = 0.025 => Q[0,1] = 0.05
# Q[1,0] = Q[0,1] = 0.05 (symmetric)
# Q[0,0] = 0, Q[1,1] = 0
# c[0] = -0.06 (coefficient of x1 in linear part of -Z)
# c[1] = -0.04 (coefficient of x2 in linear part of -Z)
# Wait, the objective to minimize is -Z = -2.296 - 0.04*x2 + 0.06*x1 + 0.025*x1*x2
# So c = [0.06, -0.04] for the linear terms (excluding constant)
# And the quadratic term is 0.025*x1*x2

Q = np.array([[0.0, 0.05], [0.05, 0.0]])
c = np.array([0.06, -0.04])

# Enumerate all 4 binary combinations
best_val = -np.inf
best_x = None

for x1 in [0, 1]:
    for x2 in [0, 1]:
        x = np.array([x1, x2])
        # Compute Z = 2.296 + 0.04*x2 - 0.06*x1 - 0.025*x1*x2
        Z = 2.296 + 0.04 * x2 - 0.06 * x1 - 0.025 * x1 * x2
        if Z > best_val:
            best_val = Z
            best_x = x

print("OPTIMAL_VALUE:", best_val)