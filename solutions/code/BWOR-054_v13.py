from ortools.linear_solver import pywraplp

# Index sets
I = [1, 2, 3, 4, 5, 6]
D = [1, 2, 3, 4, 5]

# Parameters
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

T_open = 14
L = dict()
for i in [1, 2, 3, 4]:
    L[i] = 8
for i in [5, 6]:
    L[i] = 7

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
y = dict()
for i in I:
    for d in D:
        x[i, d] = solver.NumVar(0, H[i, d], 'x_{}_{}'.format(i, d))
        y[i, d] = solver.BoolVar('y_{}_{}'.format(i, d))

# Objective: minimize total wage
obj = sum(w[i] * x[i, d] for i in I for d in D)
solver.Minimize(obj)

# Constraint 1: Coverage - total hours per day equals 14
for d in D:
    solver.Add(sum(x[i, d] for i in I) == T_open)

# Constraint 2: Maximum daily work hours (already enforced by upper bound, but add explicitly)
for i in I:
    for d in D:
        solver.Add(x[i, d] <= H[i, d])

# Constraint 3: Minimum weekly work hours
for i in I:
    solver.Add(sum(x[i, d] for d in D) >= L[i])

# Constraint 4: Maximum days assigned per week (no more than 2 days)
for i in I:
    solver.Add(sum(y[i, d] for d in D) <= 2)

# Constraint 5: Linking constraints (Big-M)
for i in I:
    for d in D:
        solver.Add(x[i, d] <= H[i, d] * y[i, d])

# Constraint 6: Maximum students per day (no more than 3)
for d in D:
    solver.Add(sum(y[i, d] for i in I) <= 3)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")