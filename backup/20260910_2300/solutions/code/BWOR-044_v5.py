from ortools.linear_solver import pywraplp

# Define index sets
I = [1, 2, 3]
J = ['A', 'B', 'C']

# Parameters
c = dict()
c[1, 'A'] = 1
c[1, 'B'] = 2
c[1, 'C'] = 2
c[2, 'A'] = 1
c[2, 'B'] = 4
c[2, 'C'] = 5
c[3, 'A'] = 2
c[3, 'B'] = 3
c[3, 'C'] = 3

s = dict()
s[1] = 20
s[2] = 40
s[3] = 30

d = dict()
d['A'] = 30
d['B'] = 20
d['C'] = 20

h = dict()
h[1] = 5
h[2] = 4
h[3] = 3

L = dict()
L[2] = 38
L[3] = 27

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    raise ValueError("Failed to create GLOP solver")

inf = solver.infinity()

# Decision variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, inf, 'x_' + str(i) + '_' + j)

u = dict()
for i in I:
    u[i] = solver.NumVar(0, inf, 'u_' + str(i))

# Objective function
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(c[i, j] * x[i, j])
for i in I:
    obj_terms.append(h[i] * u[i])

solver.Minimize(sum(obj_terms))

# Supply balance constraints
for i in I:
    constraint = sum(x[i, j] for j in J) + u[i] == s[i]
    solver.Add(constraint)

# Demand satisfaction constraints
for j in J:
    constraint = sum(x[i, j] for i in I) == d[j]
    solver.Add(constraint)

# Minimum shipment constraints
for i in [2, 3]:
    constraint = sum(x[i, j] for j in J) >= L[i]
    solver.Add(constraint)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")