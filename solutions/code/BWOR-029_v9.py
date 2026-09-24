from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
shifts = [1, 2, 3, 4, 5, 6]
blocks = [1, 2, 3, 4, 5, 6]

# Parameters
C_ft = 80
C_ct = 120

D = dict()
D[1] = 10
D[2] = 15
D[3] = 25
D[4] = 20
D[5] = 18
D[6] = 12

# Shift-to-block coverage: shift s covers blocks (s mod 6) and ((s mod 6) + 1) mod 6
# Shift 1 (start 2:00): covers B1, B2
# Shift 2 (start 6:00): covers B2, B3
# Shift 3 (start 10:00): covers B3, B4
# Shift 4 (start 14:00): covers B4, B5
# Shift 5 (start 18:00): covers B5, B6
# Shift 6 (start 22:00): covers B6, B1

A = dict()
for s in shifts:
    for b in blocks:
        A[s, b] = 0

# Shift 1 covers B1, B2
A[1, 1] = 1
A[1, 2] = 1
# Shift 2 covers B2, B3
A[2, 2] = 1
A[2, 3] = 1
# Shift 3 covers B3, B4
A[3, 3] = 1
A[3, 4] = 1
# Shift 4 covers B4, B5
A[4, 4] = 1
A[4, 5] = 1
# Shift 5 covers B5, B6
A[5, 5] = 1
A[5, 6] = 1
# Shift 6 covers B6, B1
A[6, 6] = 1
A[6, 1] = 1

# Decision variables
x = dict()
y = dict()
for s in shifts:
    x[s] = solver.IntVar(0, solver.infinity(), 'x_' + str(s))
    y[s] = solver.IntVar(0, solver.infinity(), 'y_' + str(s))

# Objective: minimize total cost
obj = 0
for s in shifts:
    obj += C_ft * x[s] + C_ct * y[s]
solver.Minimize(obj)

# Coverage constraints for each block
for b in blocks:
    expr = 0
    for s in shifts:
        expr += A[s, b] * (x[s] + y[s])
    solver.Add(expr >= D[b])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")