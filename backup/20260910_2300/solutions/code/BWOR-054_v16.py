from ortools.linear_solver import pywraplp

# Data
I = [1, 2, 3, 4, 5, 6]
T = [1, 2, 3, 4, 5]
I_ug = [1, 2, 3, 4]
I_grad = [5, 6]

w = dict()
w[1] = 10.0
w[2] = 10.0
w[3] = 9.9
w[4] = 9.8
w[5] = 10.8
w[6] = 11.3

# a[i][t] = max daily hours for student i on day t
a = dict()
a[1] = dict()
a[1][1] = 6
a[1][2] = 0
a[1][3] = 9
a[1][4] = 0
a[1][5] = 7
a[2] = dict()
a[2][1] = 0
a[2][2] = 9
a[2][3] = 0
a[2][4] = 6
a[2][5] = 0
a[3] = dict()
a[3][1] = 4
a[3][2] = 8
a[3][3] = 3
a[3][4] = 0
a[3][5] = 5
a[4] = dict()
a[4][1] = 5
a[4][2] = 5
a[4][3] = 6
a[4][4] = 0
a[4][5] = 4
a[5] = dict()
a[5][1] = 3
a[5][2] = 0
a[5][3] = 4
a[5][4] = 8
a[5][5] = 0
a[6] = dict()
a[6][1] = 0
a[6][2] = 9
a[6][3] = 0
a[6][4] = 6
a[6][5] = 3

H_day = 16
M_ug = 8
M_grad = 7
K_max = 3
S_max = 2

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x = dict()
y = dict()
for i in I:
    for t in T:
        x[i, t] = solver.NumVar(0, a[i][t], 'x_' + str(i) + '_' + str(t))
        y[i, t] = solver.BoolVar('y_' + str(i) + '_' + str(t))

# Objective: minimize total wage cost
obj_terms = []
for i in I:
    for t in T:
        obj_terms.append(w[i] * x[i, t])
solver.Minimize(sum(obj_terms))

# Constraint 1: Coverage - sum of hours per day = 16
for t in T:
    solver.Add(sum(x[i, t] for i in I) == H_day)

# Constraint 2: Linking x and y
for i in I:
    for t in T:
        solver.Add(x[i, t] <= a[i][t] * y[i, t])

# Constraint 3: Minimum weekly hours - Undergraduate
for i in I_ug:
    solver.Add(sum(x[i, t] for t in T) >= M_ug)

# Constraint 4: Minimum weekly hours - Graduate
for i in I_grad:
    solver.Add(sum(x[i, t] for t in T) >= M_grad)

# Constraint 5: Max duty shifts per student per week
for i in I:
    solver.Add(sum(y[i, t] for t in T) <= S_max)

# Constraint 6: Max students scheduled per day
for t in T:
    solver.Add(sum(y[i, t] for i in I) <= K_max)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")