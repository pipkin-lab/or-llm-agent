import math
from ortools.linear_solver import pywraplp

# Parameters
# Coordinates (1-indexed: village 1 through 8)
coords = dict()
coords[1] = (0, 0)
coords[2] = (10, 3)
coords[3] = (12, 15)
coords[4] = (14, 13)
coords[5] = (16, 9)
coords[6] = (18, 6)
coords[7] = (8, 12)
coords[8] = (6, 10)

# Number of students per village
n = dict()
n[1] = 60
n[2] = 80
n[3] = 100
n[4] = 120
n[5] = 80
n[6] = 60
n[7] = 40
n[8] = 80

# Index sets
I = list(range(1, 9))  # villages 1 through 8
J = list(range(1, 9))  # potential school locations 1 through 8
K = 2

# Pre-compute Euclidean distances d[i][j]
d = dict()
for i in I:
    for j in J:
        xi, yi = coords[i]
        xj, yj = coords[j]
        d[i, j] = math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

# Create solver (MILP)
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
S = dict()
for j in J:
    S[j] = solver.BoolVar('S_' + str(j))

A = dict()
for i in I:
    for j in J:
        A[i, j] = solver.BoolVar('A_' + str(i) + '_' + str(j))

# Objective: minimize total weighted walking distance
objective_terms = []
for i in I:
    for j in J:
        objective_terms.append(n[i] * d[i, j] * A[i, j])

solver.Minimize(sum(objective_terms))

# Constraint 1: Exactly K schools are built
solver.Add(sum(S[j] for j in J) == K)

# Constraint 2: Each village is assigned to exactly one school
for i in I:
    solver.Add(sum(A[i, j] for j in J) == 1)

# Constraint 3: Assignment feasibility
for i in I:
    for j in J:
        solver.Add(A[i, j] <= S[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")