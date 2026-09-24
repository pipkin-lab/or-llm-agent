from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    print("Could not create solver")
    exit(1)

# Data
I = [1, 2, 3, 4, 5, 6]
D = [1, 2, 3, 4, 5]

w = dict()
w[1] = 10.0
w[2] = 10.0
w[3] = 9.9
w[4] = 9.8
w[5] = 10.8
w[6] = 11.3

H = dict()
H[1, 1] = 6
H[1, 2] = 0
H[1, 3] = 9
H[1, 4] = 0
H[1, 5] = 7

H[2, 1] = 0
H[2, 2] = 9
H[2, 3] = 0
H[2, 4] = 6
H[2, 5] = 0

H[3, 1] = 4
H[3, 2] = 8
H[3, 3] = 3
H[3, 4] = 0
H[3, 5] = 5

H[4, 1] = 5
H[4, 2] = 5
H[4, 3] = 6
H[4, 4] = 0
H[4, 5] = 4

H[5, 1] = 3
H[5, 2] = 0
H[5, 3] = 4
H[5, 4] = 8
H[5, 5] = 0

H[6, 1] = 0
H[6, 2] = 9
H[6, 3] = 0
H[6, 4] = 6
H[6, 5] = 3

L_min = dict()
for i in I:
    if i <= 4:
        L_min[i] = 8
    else:
        L_min[i] = 7

T_daily = 14

# Decision variables x[i, d]
x = dict()
for i in I:
    for d in D:
        x[i, d] = solver.NumVar(0, H[i, d], 'x_' + str(i) + '_' + str(d))

# Objective: minimize total wage
obj_terms = []
for i in I:
    for d in D:
        obj_terms.append(w[i] * x[i, d])
objective = sum(obj_terms)
solver.Minimize(objective)

# Daily coverage constraints
for d in D:
    coverage = sum(x[i, d] for i in I)
    solver.Add(coverage == T_daily)

# Minimum weekly work hours constraints
for i in I:
    weekly = sum(x[i, d] for d in D)
    solver.Add(weekly >= L_min[i])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")