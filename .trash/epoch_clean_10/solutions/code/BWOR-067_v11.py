from ortools.linear_solver import pywraplp

# Initialize the LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')
infinity = solver.infinity()

# Parameters
T = [0, 1, 2]  # Months 1, 2, 3 (0-indexed)
K = 200         # Number of segments
delta = 1       # Segment width

# Demands for months 1, 2, 3
d = [100, 110, 120]

# Holding cost per unit per month
h = 1

# Marginal cost for segment k (1-indexed): mc_k = 2k - 1
# We'll compute on the fly: for segment index k (0-indexed), marginal cost = 2*(k+1) - 1 = 2k + 1

# Decision Variables
# z[t, k]: amount of production in month t allocated to segment k (0 <= z <= delta)
z = dict()
for t in T:
    for k in range(K):
        z[t, k] = solver.NumVar(0, delta, 'z_' + str(t) + '_' + str(k))

# x[t]: total production in month t
x = dict()
for t in T:
    x[t] = solver.NumVar(0, infinity, 'x_' + str(t))

# I[t]: inventory at end of month t
I = dict()
for t in T:
    I[t] = solver.NumVar(0, infinity, 'I_' + str(t))

# Constraints

# 1. Production definition: x[t] = sum_k z[t, k]
for t in T:
    solver.Add(x[t] == sum(z[t, k] for k in range(K)))

# 2. Inventory balance: I[t] = I[t-1] + x[t] - d[t]
# For t=0: I[0] = 0 + x[0] - d[0]
solver.Add(I[0] == x[0] - d[0])
# For t=1: I[1] = I[0] + x[1] - d[1]
solver.Add(I[1] == I[0] + x[1] - d[1])
# For t=2: I[2] = I[1] + x[2] - d[2]
solver.Add(I[2] == I[1] + x[2] - d[2])

# 3. Final inventory must be 0
solver.Add(I[2] == 0)

# Objective: Minimize total production cost + total holding cost
obj = 0
for t in T:
    for k in range(K):
        mc_k = 2 * (k + 1) - 1  # marginal cost for segment k (1-indexed)
        obj += mc_k * z[t, k]
    obj += h * I[t]

solver.Minimize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")