from ortools.linear_solver import pywraplp

# Define index sets
I = [1, 2, 3, 4]          # Undergraduate students
G = [5, 6]                # Graduate students
J = [1, 2, 3, 4, 5, 6]   # All students
D = [1, 2, 3, 4, 5]       # Days (Mon-Fri)

# Parameters
w = dict()
w[1] = 10.0
w[2] = 10.0
w[3] = 9.9
w[4] = 9.8
w[5] = 10.8
w[6] = 11.3

M = dict()
# Student 1
M[1, 1] = 6
M[1, 2] = 0
M[1, 3] = 9
M[1, 4] = 0
M[1, 5] = 7
# Student 2
M[2, 1] = 0
M[2, 2] = 9
M[2, 3] = 0
M[2, 4] = 6
M[2, 5] = 0
# Student 3
M[3, 1] = 4
M[3, 2] = 8
M[3, 3] = 3
M[3, 4] = 0
M[3, 5] = 5
# Student 4
M[4, 1] = 5
M[4, 2] = 5
M[4, 3] = 6
M[4, 4] = 0
M[4, 5] = 4
# Student 5
M[5, 1] = 3
M[5, 2] = 0
M[5, 3] = 4
M[5, 4] = 8
M[5, 5] = 0
# Student 6
M[6, 1] = 0
M[6, 2] = 9
M[6, 3] = 0
M[6, 4] = 6
M[6, 5] = 3

H = dict()
for d in D:
    H[d] = 14

L_min_UG = 8
L_min_Grad = 7

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: x[j, d] >= 0
x = dict()
for j in J:
    for d in D:
        x[j, d] = solver.NumVar(0, M[j, d], 'x_' + str(j) + '_' + str(d))

# Objective: Minimize total wage payment
obj = 0
for j in J:
    for d in D:
        obj += w[j] * x[j, d]

solver.Minimize(obj)

# Constraint 1: Daily coverage
for d in D:
    solver.Add(sum(x[j, d] for j in J) == H[d])

# Constraint 3: Minimum weekly workload
for j in I:
    solver.Add(sum(x[j, d] for d in D) >= L_min_UG)

for j in G:
    solver.Add(sum(x[j, d] for d in D) >= L_min_Grad)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")