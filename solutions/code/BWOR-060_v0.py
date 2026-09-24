import math
from ortools.linear_solver import pywraplp

# Problem parameters
I = list(range(1, 9))  # Villages 1 to 8
J = list(range(1, 9))  # Candidate school locations 1 to 8
K = 2                  # Number of schools to build

# Coordinates
x_coords = {
    1: 0, 2: 10, 3: 12, 4: 14, 5: 16, 6: 18, 7: 8, 8: 6
}
y_coords = {
    1: 0, 2: 3, 3: 15, 4: 13, 5: 9, 6: 6, 7: 12, 8: 10
}

# Number of primary school students in each village
N = {
    1: 60, 2: 80, 3: 100, 4: 120, 5: 80, 6: 60, 7: 40, 8: 80
}

# Compute cost matrix C[i][j] = N_i * distance(i, j)
C = dict()
for i in I:
    C[i] = dict()
    for j in J:
        dist = math.sqrt((x_coords[i] - x_coords[j]) ** 2 + (y_coords[i] - y_coords[j]) ** 2)
        C[i][j] = N[i] * dist

# Create solver (MILP)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
# z[j]: 1 if school is built in village j
z = dict()
for j in J:
    z[j] = solver.BoolVar('z_' + str(j))

# w[i][j]: 1 if students from village i are assigned to school in village j
w = dict()
for i in I:
    w[i] = dict()
    for j in J:
        w[i][j] = solver.BoolVar('w_' + str(i) + '_' + str(j))

# Constraints

# 1. Exactly K schools must be built
solver.Add(sum(z[j] for j in J) == K)

# 2. Each village must be assigned to exactly one school
for i in I:
    solver.Add(sum(w[i][j] for j in J) == 1)

# 3. Students can only be assigned to a village if a school is built there
for i in I:
    for j in J:
        solver.Add(w[i][j] <= z[j])

# Objective: Minimize total walking distance
objective = 0
for i in I:
    for j in J:
        objective += C[i][j] * w[i][j]

solver.Minimize(objective)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")