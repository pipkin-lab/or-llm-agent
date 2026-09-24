from ortools.linear_solver import pywraplp

# Index sets
I = [1, 2, 3]
X = [0, 1, 2, 3]
Y = [0, 1, 2, 3]

# Parameters
R1 = 3
R2 = 3

# Profit tables P[i][y][x]
P = dict()
P[1] = dict()
P[1][0] = [0, 4, 5, 6]
P[1][1] = [1, 5, 6, 7]
P[1][2] = [3, 6, 7, 8]
P[1][3] = [6, 7, 8, 9]

P[2] = dict()
P[2][0] = [0, 1, 4, 6]
P[2][1] = [2, 4, 6, 8]
P[2][2] = [4, 6, 8, 10]
P[2][3] = [6, 7, 9, 11]

P[3] = dict()
P[3][0] = [0, 2, 4, 6]
P[3][1] = [3, 5, 7, 9]
P[3][2] = [5, 7, 9, 11]
P[3][3] = [8, 9, 11, 13]

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables z[i, x, y]
z = dict()
for i in I:
    for x in X:
        for y in Y:
            z[i, x, y] = solver.BoolVar('z_{}_{}_{}'.format(i, x, y))

# Objective: Maximize total profit
obj = 0
for i in I:
    for x in X:
        for y in Y:
            obj += P[i][y][x] * z[i, x, y]

solver.Maximize(obj)

# Constraint 1: Each department gets exactly one (x, y) combination
for i in I:
    expr = 0
    for x in X:
        for y in Y:
            expr += z[i, x, y]
    solver.Add(expr == 1)

# Constraint 2: Total Resource 1 allocated <= R1
expr_r1 = 0
for i in I:
    for x in X:
        for y in Y:
            if x > 0:
                expr_r1 += x * z[i, x, y]
    if expr_r1 == 0:
        pass
    else:
        solver.Add(expr_r1 <= R1)

# Constraint 3: Total Resource 2 allocated <= R2
expr_r2 = 0
for i in I:
    for x in X:
        for y in Y:
            if y > 0:
                expr_r2 += y * z[i, x, y]
    if expr_r2 == 0:
        pass
    else:
        solver.Add(expr_r2 <= R2)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")