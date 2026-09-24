from ortools.linear_solver import pywraplp

# Parameters
T = [1, 2, 3, 4]

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

c = dict()
c[1] = 12.0
c[2] = 11.0
c[3] = 11.5
c[4] = 12.5

h = 0.1

# Decision variables: x[p, i] for p <= i
x = dict()
for p in T:
    for i in T:
        if p <= i:
            x[p, i] = None  # placeholder, will be replaced below

# Actually, we need to create variables. Let's do it properly.
x = dict()
for p in T:
    for i in T:
        if p <= i:
            x[p, i] = None  # We'll assign solver variables below

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Create variables
x = dict()
for p in T:
    for i in T:
        if p <= i:
            x[p, i] = solver.NumVar(0, INF, 'x_{}_{}'.format(p, i))

# Objective function
obj = 0
for p in T:
    for i in T:
        if p <= i:
            H = h * (i - p)
            obj += (c[p] + H) * x[p, i]

solver.Minimize(obj)

# Production capacity constraints
for p in T:
    solver.Add(sum(x[p, i] for i in T if i >= p) <= C[p])

# Delivery demand constraints
for i in T:
    solver.Add(sum(x[p, i] for p in T if p <= i) == D[i])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")