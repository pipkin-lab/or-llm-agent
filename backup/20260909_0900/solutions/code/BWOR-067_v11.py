from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
d = [0, 100, 110, 120]  # 1-indexed: d[1], d[2], d[3]
s0 = 0
s3_final = 0
h = 1

# Decision Variables
# x_t: production in month t (continuous, >= 0)
# s_t: ending inventory at month t (continuous, >= 0)
x = dict()
s = dict()

for t in range(1, 4):
    x[t] = solver.NumVar(0, solver.infinity(), 'x_' + str(t))
    s[t] = solver.NumVar(0, solver.infinity(), 's_' + str(t))

# Inventory Balance Constraints
# s_1 = s_0 + x_1 - d_1
solver.Add(s[1] == s0 + x[1] - d[1])

# s_2 = s_1 + x_2 - d_2
solver.Add(s[2] == s[1] + x[2] - d[2])

# s_3 = s_2 + x_3 - d_3
solver.Add(s[3] == s[2] + x[3] - d[3])

# Boundary Condition: s_3 = 0
solver.Add(s[3] == s3_final)

# Objective Function: Minimize sum(x_t^2) + sum(h * s_t)
# Since pywraplp does not support quadratic objectives directly, we use a Piecewise Linear Approximation (PWLA)
# for the convex function f(x) = x^2.
# We approximate x^2 over the range [0, M] where M is an upper bound for production.
# A reasonable upper bound for production in any month is the total demand (330) since no initial/final stock is required.
# Let's use M = 330 for each x_t.
# We will use a PWLA with segments. Let's use 100 segments for good approximation.
# For f(x) = x^2, the derivative is 2x.
# Segment k (0-indexed) covers [k*delta, (k+1)*delta]
# The slope in segment k is approximately the average derivative: (2*(k*delta + delta/2)) = 2*k*delta + delta
# Actually, for convex PWLA, we define segments with increasing slopes.
# Let's define K segments, each of width Delta.
# Let M = 330. Let K = 330 (so Delta = 1). This gives a very accurate approximation.
# Or K = 100, Delta = 3.3. Let's use integer steps for simplicity if possible, but Delta can be float.
# Let's use K = 100 segments for x in [0, 330]. Delta = 3.3.
# To avoid floating point issues in bounds, let's use a larger M or different K.
# Let's use M = 400, K = 100, Delta = 4.
# The function value at the start of segment k is f(k*Delta).
# The slope of segment k is (f((k+1)*Delta) - f(k*Delta)) / Delta.
# We introduce variables z[t, k] representing the amount of production in segment k for month t.
# x[t] = sum(k) z[t, k]
# 0 <= z[t, k] <= Delta
# Cost contribution for segment k is slope_k * z[t, k]

M = 400
K = 100
Delta = M / K

# Pre-calculate slopes for f(x) = x^2
slopes = [0.0] * K
for k in range(K):
    x_start = k * Delta
    x_end = (k + 1) * Delta
    f_start = x_start * x_start
    f_end = x_end * x_end
    slopes[k] = (f_end - f_start) / Delta

# Create segment variables z[t, k]
z = dict()
for t in range(1, 4):
    for k in range(K):
        z[t, k] = solver.NumVar(0, Delta, 'z_' + str(t) + '_' + str(k))

# Link x[t] to z[t, k]
for t in range(1, 4):
    solver.Add(x[t] == sum(z[t, k] for k in range(K)))

# Objective:
# Production cost: sum over t, sum over k (slopes[k] * z[t, k])
# Holding cost: h * (s[1] + s[2] + s[3])
# Note: s[3] is fixed to 0, so its contribution is 0.

prod_cost = 0
for t in range(1, 4):
    for k in range(K):
        prod_cost += slopes[k] * z[t, k]

hold_cost = h * (s[1] + s[2] + s[3])

obj = prod_cost + hold_cost

solver.Minimize(obj)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # The objective value is the approximate total cost.
    # However, the prompt asks for the "OPTIMAL_VALUE" which is the minimized Z.
    # Since we used PWLA, the objective value from the solver is the approximate cost.
    # For a quadratic objective, the true value is x1^2 + x2^2 + x3^2 + s1 + s2 + s3.
    # Let's reconstruct the true quadratic value using the optimal x values for higher precision,
    # as the PWLA is an approximation.
    x1_val = x[1].solution_value()
    x2_val = x[2].solution_value()
    x3_val = x[3].solution_value()
    s1_val = s[1].solution_value()
    s2_val = s[2].solution_value()
    s3_val = s[3].solution_value()
    
    true_obj = x1_val * x1_val + x2_val * x2_val + x3_val * x3_val + h * (s1_val + s2_val + s3_val)
    print("OPTIMAL_VALUE:", true_obj)
else:
    print("NO_FEASIBLE_SOLUTION")