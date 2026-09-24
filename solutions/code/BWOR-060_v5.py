import math
from ortools.linear_solver import pywraplp

# Index sets
N = [1, 2, 3, 4, 5, 6, 7, 8]

# Parameters: student counts
n = dict()
n[1] = 60
n[2] = 80
n[3] = 100
n[4] = 120
n[5] = 80
n[6] = 60
n[7] = 40
n[8] = 80

# Parameters: coordinates
coords = dict()
coords[1] = (0, 0)
coords[2] = (10, 3)
coords[3] = (12, 15)
coords[4] = (14, 13)
coords[5] = (16, 9)
coords[6] = (18, 6)
coords[7] = (8, 12)
coords[8] = (6, 10)

# Pre-compute Euclidean distances
d = dict()
for i in N:
    for j in N:
        dx = coords[i][0] - coords[j][0]
        dy = coords[i][1] - coords[j][1]
        d[i, j] = math.sqrt(dx * dx + dy * dy)

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
y = dict()
for j in N:
    y[j] = solver.BoolVar('y_' + str(j))

z = dict()
for i in N:
    for j in N:
        z[i, j] = solver.BoolVar('z_' + str(i) + '_' + str(j))

# Constraints
# 1. Exactly two schools are built
solver.Add(sum(y[j] for j in N) == 2)

# 2. Each village's students are assigned to exactly one school
for i in N:
    solver.Add(sum(z[i, j] for j in N) == 1)

# 3. Students can only be assigned to a school if one is built there
for i in N:
    for j in N:
        solver.Add(z[i, j] <= y[j])

# Objective: Minimize total weighted walking distance
obj = sum(n[i] * d[i, j] * z[i, j] for i in N for j in N)
solver.Minimize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")