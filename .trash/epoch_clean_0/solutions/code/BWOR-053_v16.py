from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Index sets
I = [1, 2, 3, 4, 5, 6]
D = [1, 2, 3, 4, 5]
I_U = [1, 2, 3, 4]
I_G = [5, 6]

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

H_req = 14
L_U = 8
L_G = 7

# Decision variables
x = dict()
for i in I:
    for d in D:
        x[i, d] = solver.NumVar(0, M[i, d], 'x_' + str(i) + '_' + str(d))

# Objective: minimize total weekly wage
obj = 0
for i in I:
    for d in D:
        obj += w[i] * x[i, d]

solver.Minimize(obj)

# Daily coverage constraints
for d in D:
    solver.Add(sum(x[i, d] for i in I) == H_req)

# Maximum availability constraints (already enforced by upper bounds, but add explicitly for clarity)
for i in I:
    for d in D:
        solver.Add(x[i, d] <= M[i, d])

# Minimum weekly hours for undergraduates
for i in I_U:
    solver.Add(sum(x[i, d] for d in D) >= L_U)

# Minimum weekly hours for graduates
for i in I_G:
    solver.Add(sum(x[i, d] for d in D) >= L_G)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")