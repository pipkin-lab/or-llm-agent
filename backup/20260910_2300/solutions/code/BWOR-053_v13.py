from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Index sets
I = [1, 2, 3, 4, 5, 6]
D = [1, 2, 3, 4, 5]
I_ug = [1, 2, 3, 4]
I_gr = [5, 6]

# Parameters
w = dict()
w[1] = 10.0
w[2] = 10.0
w[3] = 9.9
w[4] = 9.8
w[5] = 10.8
w[6] = 11.3

M = dict()
# M[i, d] = max hours for student i on day d
# Row 1: 6, 0, 9, 0, 7
M[1, 1] = 6
M[1, 2] = 0
M[1, 3] = 9
M[1, 4] = 0
M[1, 5] = 7
# Row 2: 0, 9, 0, 6, 0
M[2, 1] = 0
M[2, 2] = 9
M[2, 3] = 0
M[2, 4] = 6
M[2, 5] = 0
# Row 3: 4, 8, 3, 0, 5
M[3, 1] = 4
M[3, 2] = 8
M[3, 3] = 3
M[3, 4] = 0
M[3, 5] = 5
# Row 4: 5, 5, 6, 0, 4
M[4, 1] = 5
M[4, 2] = 5
M[4, 3] = 6
M[4, 4] = 0
M[4, 5] = 4
# Row 5: 3, 0, 4, 8, 0
M[5, 1] = 3
M[5, 2] = 0
M[5, 3] = 4
M[5, 4] = 8
M[5, 5] = 0
# Row 6: 0, 9, 0, 6, 3
M[6, 1] = 0
M[6, 2] = 9
M[6, 3] = 0
M[6, 4] = 6
M[6, 5] = 3

H_day = 14

# Decision variables
x = dict()
for i in I:
    for d in D:
        x[i, d] = solver.NumVar(0, M[i, d], 'x_' + str(i) + '_' + str(d))

# Objective function: minimize total wage
obj = 0
for i in I:
    for d in D:
        obj += w[i] * x[i, d]
solver.Minimize(obj)

# Constraint A: Daily staffing requirement
for d in D:
    solver.Add(sum(x[i, d] for i in I) == H_day)

# Constraint B: Individual daily availability (already handled by upper bound, but explicit for clarity)
for i in I:
    for d in D:
        solver.Add(x[i, d] <= M[i, d])

# Constraint C: Minimum weekly hours for undergraduates
for i in I_ug:
    solver.Add(sum(x[i, d] for d in D) >= 8)

# Constraint D: Minimum weekly hours for graduates
for i in I_gr:
    solver.Add(sum(x[i, d] for d in D) >= 7)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")