from ortools.linear_solver import pywraplp

# Parameters
T = [1, 2, 3]
d = {1: 100, 2: 110, 3: 120}
h = 1
s0 = 0
Xmax = 330  # sum of all demands
K = 330     # number of segments

# Solver (LP since all variables are continuous)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision Variables
# z[t, k]: amount of production in month t allocated to segment k, 0 <= z[t,k] <= 1
z = dict()
for t in T:
    for k in range(1, K + 1):
        z[t, k] = solver.NumVar(0, 1, 'z_' + str(t) + '_' + str(k))

# x[t]: total production in month t
x = dict()
for t in T:
    x[t] = solver.NumVar(0, Xmax, 'x_' + str(t))

# s[t]: inventory at end of month t
s = dict()
for t in T:
    s[t] = solver.NumVar(0, Xmax, 's_' + str(t))

# Constraints

# 1. Production linkage: x[t] = sum of z[t, k]
for t in T:
    solver.Add(x[t] == sum(z[t, k] for k in range(1, K + 1)))

# 2. Inventory balance: s[t] = s[t-1] + x[t] - d[t]
# s0 = 0
solver.Add(s[1] == s0 + x[1] - d[1])
solver.Add(s[2] == s[1] + x[2] - d[2])
solver.Add(s[3] == s[2] + x[3] - d[3])

# 3. Final inventory constraint: s[3] = 0
solver.Add(s[3] == 0)

# Objective: Minimize total production cost + holding cost
# Production cost for month t: sum over k of (2k - 1) * z[t, k]
# Holding cost: h * s[t] for t in T
obj = 0
for t in T:
    for k in range(1, K + 1):
        obj += (2 * k - 1) * z[t, k]
    obj += h * s[t]

solver.Minimize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")