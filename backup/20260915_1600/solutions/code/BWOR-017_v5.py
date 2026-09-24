from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index sets
P = [1, 2, 3]
R = [1, 2, 3]

# Parameters
a = dict()
a[1, 1] = 2
a[1, 2] = 4
a[1, 3] = 8
a[2, 1] = 2
a[2, 2] = 3
a[2, 3] = 4
a[3, 1] = 1
a[3, 2] = 2
a[3, 3] = 3

b = dict()
b[1] = 500
b[2] = 300
b[3] = 100

c = dict()
c[1] = 4
c[2] = 5
c[3] = 6

s = dict()
s[1] = 8
s[2] = 10
s[3] = 12

F = dict()
F[1] = 100
F[2] = 150
F[3] = 200

M = dict()
M[1] = 100
M[2] = 50
M[3] = 100 / 3

# Decision variables
x = dict()
y = dict()
for p in P:
    x[p] = solver.NumVar(0, INF, 'x_' + str(p))
    y[p] = solver.BoolVar('y_' + str(p))

# Objective: maximize total profit
obj_terms = []
for p in P:
    obj_terms.append((s[p] - c[p]) * x[p])
    obj_terms.append(-F[p] * y[p])
obj = sum(obj_terms)
solver.Maximize(obj)

# Resource availability constraints
for r in R:
    solver.Add(sum(a[r, p] * x[p] for p in P) <= b[r])

# Linking constraints: x_p <= M_p * y_p
for p in P:
    solver.Add(x[p] <= M[p] * y[p])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")