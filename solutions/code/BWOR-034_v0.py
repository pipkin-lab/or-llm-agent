from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
R = dict()
R[1] = 1500
R[2] = 1000
R[3] = 2000
R[4] = 1200

c = dict()
c[1] = 28
c[2] = 45
c[3] = 60
c[4] = 73

# Valid (t, d) pairs
valid_pairs = [
    (1, 1), (1, 2), (1, 3), (1, 4),
    (2, 1), (2, 2), (2, 3),
    (3, 1), (3, 2),
    (4, 1)
]

# Decision variables
x = dict()
for (t, d) in valid_pairs:
    x[t, d] = solver.NumVar(0, INF, 'x_{}_{}'.format(t, d))

# Objective: minimize total rental cost
obj = 0
for (t, d) in valid_pairs:
    obj += c[d] * x[t, d]
solver.Minimize(obj)

# Coverage constraints for each month m
for m in [1, 2, 3, 4]:
    # A contract (t, d) is active in month m if t <= m <= t + d - 1
    expr = 0
    for (t, d) in valid_pairs:
        if t <= m <= t + d - 1:
            expr += x[t, d]
    solver.Add(expr >= R[m])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")