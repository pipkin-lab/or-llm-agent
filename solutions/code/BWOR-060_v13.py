import math
from ortools.linear_solver import pywraplp

# Index sets
V = list(range(8))  # Villages 0-7 (0-indexed in code, but model uses 1-8)
# We'll use 0-indexed internally for Python convenience, mapping to the given data

# Parameters
x = [0, 10, 12, 14, 16, 18, 8, 6]
y = [0, 3, 15, 13, 9, 6, 12, 10]
s = [60, 80, 100, 120, 80, 60, 40, 80]

# Precompute distances d[i][j]
d = dict()
for i in V:
    for j in V:
        d[i, j] = math.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
z = dict()
for i in V:
    z[i] = solver.BoolVar('z_' + str(i))

w = dict()
for i in V:
    for j in V:
        if i != j:
            w[i, j] = solver.NumVar(0, s[j], 'w_' + str(i) + '_' + str(j))

u = dict()
for i in V:
    for j in V:
        if i != j:
            u[i, j] = solver.NumVar(0, INF, 'u_' + str(i) + '_' + str(j))

# Objective: Minimize total walking distance
obj = sum(u[i, j] for i in V for j in V if i != j)
solver.Minimize(obj)

# Constraint 1: Exactly two schools
solver.Add(sum(z[i] for i in V) == 2)

# Constraint 2: Every student assigned to exactly one school
for j in V:
    solver.Add(sum(w[i, j] for i in V if i != j) == s[j])

# Constraint 3: Capacity/Linking - w[i,j] <= s[j] * z[i]
for i in V:
    for j in V:
        if i != j:
            solver.Add(w[i, j] <= s[j] * z[i])

# Constraint 4: Distance calculation - u[i,j] = d[i,j] * w[i,j]
for i in V:
    for j in V:
        if i != j:
            solver.Add(u[i, j] == d[i, j] * w[i, j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")