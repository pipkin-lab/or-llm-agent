from ortools.linear_solver import pywraplp

# Model type: LP
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets
I = [1, 2, 3, 4, 5, 6]
I_UG = [1, 2, 3, 4]
I_GR = [5, 6]
D = [1, 2, 3, 4, 5]

# Parameters
w = dict()
w[1] = 10.0
w[2] = 10.0
w[3] = 9.9
w[4] = 9.8
w[5] = 10.8
w[6] = 11.3

# M[i][d] = max available hours for student i on day d
M = dict()
M[1, 1] = 6
M[1, 2] = 0
M[1, 3] = 9
M[1, 4] = 0
M[1, 5] = 7
M[2, 1] = 0
M[2, 2] = 9
M[2, 3] = 0
M[2, 4] = 6
M[2, 5] = 0
M[3, 1] = 4
M[3, 2] = 8
M[3, 3] = 3
M[3, 4] = 0
M[3, 5] = 5
M[4, 1] = 5
M[4, 2] = 5
M[4, 3] = 6
M[4, 4] = 0
M[4, 5] = 4
M[5, 1] = 3
M[5, 2] = 0
M[5, 3] = 4
M[5, 4] = 8
M[5, 5] = 0
M[6, 1] = 0
M[6, 2] = 9
M[6, 3] = 0
M[6, 4] = 6
M[6, 5] = 3

H_min_UG = 8
H_min_GR = 7
H_day = 14

# Decision variables: x[i, d] >= 0
x = dict()
for i in I:
    for d in D:
        x[i, d] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(d))

# Objective: minimize total wage cost
obj = 0
for i in I:
    for d in D:
        obj += w[i] * x[i, d]
solver.Minimize(obj)

# Constraint 1: Daily coverage (exactly 14 hours per day)
for d in D:
    solver.Add(sum(x[i, d] for i in I) == H_day)

# Constraint 2: Maximum daily availability
for i in I:
    for d in D:
        solver.Add(x[i, d] <= M[i, d])

# Constraint 3: Minimum weekly hours - Undergraduate
for i in I_UG:
    solver.Add(sum(x[i, d] for d in D) >= H_min_UG)

# Constraint 4: Minimum weekly hours - Graduate
for i in I_GR:
    solver.Add(sum(x[i, d] for d in D) >= H_min_GR)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")