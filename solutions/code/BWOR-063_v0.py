from ortools.linear_solver import pywraplp

# Define index sets
I = [1, 2, 3]
X = [0, 1, 2, 3]
Y = [0, 1, 2, 3]

# Define profit parameters
P = dict()
P[1] = dict()
for x in X:
    P[1][x] = dict()
    P[1][x][0] = [0, 4, 5, 6][x]
    P[1][x][1] = [1, 5, 6, 7][x]
    P[1][x][2] = [3, 6, 7, 8][x]
    P[1][x][3] = [6, 7, 8, 9][x]

P[2] = dict()
for x in X:
    P[2][x] = dict()
    P[2][x][0] = [0, 1, 4, 6][x]
    P[2][x][1] = [2, 4, 6, 8][x]
    P[2][x][2] = [4, 6, 8, 10][x]
    P[2][x][3] = [6, 7, 9, 11][x]

P[3] = dict()
for x in X:
    P[3][x] = dict()
    P[3][x][0] = [0, 2, 4, 6][x]
    P[3][x][1] = [3, 5, 7, 9][x]
    P[3][x][2] = [5, 7, 9, 11][x]
    P[3][x][3] = [8, 9, 11, 13][x]

X_total = 3
Y_total = 3

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
z = dict()
for i in I:
    for x in X:
        for y in Y:
            z[i, x, y] = solver.BoolVar('z_' + str(i) + '_' + str(x) + '_' + str(y))

# Objective function
objective = 0
for i in I:
    for x in X:
        for y in Y:
            objective += P[i][x][y] * z[i, x, y]

solver.Maximize(objective)

# Constraint 1: Exclusive allocation per department
for i in I:
    expr = sum(z[i, x, y] for x in X for y in Y)
    solver.Add(expr == 1)

# Constraint 2: Resource 1 conservation
expr_r1 = sum(x * z[i, x, y] for i in I for x in X for y in Y)
solver.Add(expr_r1 == X_total)

# Constraint 3: Resource 2 conservation
expr_r2 = sum(y * z[i, x, y] for i in I for x in X for y in Y)
solver.Add(expr_r2 == Y_total)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")