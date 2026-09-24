from ortools.linear_solver import pywraplp
import math

# Parameters
n_villages = 8
n_students = [60, 80, 100, 120, 80, 60, 40, 80]
x_coords = [0, 10, 12, 14, 16, 18, 8, 6]
y_coords = [0, 3, 15, 13, 9, 6, 12, 10]
num_schools = 2

# Calculate distances
d = dict()
for i in range(n_villages):
    for j in range(n_villages):
        d[i, j] = math.sqrt((x_coords[i] - x_coords[j]) ** 2 + (y_coords[i] - y_coords[j]) ** 2)

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
z = dict()
for j in range(n_villages):
    z[j] = solver.IntVar(0, 1, 'z_' + str(j))

a = dict()
for i in range(n_villages):
    for j in range(n_villages):
        a[i, j] = solver.IntVar(0, 1, 'a_' + str(i) + '_' + str(j))

# Objective: Minimize total walking distance
obj_terms = []
for i in range(n_villages):
    for j in range(n_villages):
        obj_terms.append(n_students[i] * d[i, j] * a[i, j])

solver.Minimize(sum(obj_terms))

# Constraint 1: Exactly 2 schools
solver.Add(sum(z[j] for j in range(n_villages)) == num_schools)

# Constraint 2: Assignment to open schools only
for i in range(n_villages):
    for j in range(n_villages):
        solver.Add(a[i, j] <= z[j])

# Constraint 3: Each village assigned to exactly one school
for i in range(n_villages):
    solver.Add(sum(a[i, j] for j in range(n_villages)) == 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")