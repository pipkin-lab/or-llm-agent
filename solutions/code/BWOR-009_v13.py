from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Parameters
C = dict()
C[1] = 25
C[2] = 35
C[3] = 30
C[4] = 20

D = dict()
D[1] = 15
D[2] = 20
D[3] = 25
D[4] = 20

p = dict()
p[1] = 12.0
p[2] = 11.0
p[3] = 11.5
p[4] = 12.5

h = 0.1

# Cost matrix c[t,k] for t <= k
c = dict()
for t in range(1, 5):
    for k in range(t, 5):
        c[t, k] = p[t] + h * (k - t)

# Decision variables x[t,k] for t <= k
x = dict()
for t in range(1, 5):
    for k in range(t, 5):
        x[t, k] = solver.IntVar(0, INF, 'x_' + str(t) + '_' + str(k))

# Objective: minimize total cost
obj = 0
for t in range(1, 5):
    for k in range(t, 5):
        obj += c[t, k] * x[t, k]
solver.Minimize(obj)

# Production capacity constraints
for t in range(1, 5):
    expr = 0
    for k in range(t, 5):
        expr += x[t, k]
    solver.Add(expr <= C[t])

# Delivery demand constraints (equality)
for k in range(1, 5):
    expr = 0
    for t in range(1, k + 1):
        expr += x[t, k]
    solver.Add(expr == D[k])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")