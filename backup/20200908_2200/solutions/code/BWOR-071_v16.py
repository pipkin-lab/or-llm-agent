from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Parameters
K = 5
H = 5
Delta = 1

# Coefficients for Product A segments
a = [7, 5, 3, 1, -1]
# Coefficients for Product B segments
b = [8, 4, 0, -4, -8]

# Decision Variables
# z_A[k] for k in 0..4
z_A = dict()
for k in range(K):
    z_A[k] = solver.NumVar(0, Delta, 'z_A_' + str(k))

# z_B[k] for k in 0..4
z_B = dict()
for k in range(K):
    z_B[k] = solver.NumVar(0, Delta, 'z_B_' + str(k))

# Auxiliary variables for total quantities
x_A = solver.NumVar(0, inf, 'x_A')
x_B = solver.NumVar(0, inf, 'x_B')

# Constraints

# 1. Quantity Aggregation
# x_A = sum(z_A[k])
solver.Add(x_A == sum(z_A[k] for k in range(K)))

# x_B = sum(z_B[k])
solver.Add(x_B == sum(z_B[k] for k in range(K)))

# 2. Machine Capacity Constraint
# 1 * x_A + 1 * x_B = 5
solver.Add(x_A + x_B == H)

# Objective Function
# Maximize Z = sum(a[k] * z_A[k]) + sum(b[k] * z_B[k])
obj = sum(a[k] * z_A[k] for k in range(K)) + sum(b[k] * z_B[k] for k in range(K))

solver.Maximize(obj)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")