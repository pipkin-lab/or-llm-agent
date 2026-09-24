from ortools.linear_solver import pywraplp

# Check for missing parameters
c = dict()
for j in [1, 2, 3, 4]:
    if j == 1:
        c[j] = None
    elif j == 2:
        c[j] = None
    elif j == 3:
        c[j] = None
    elif j == 4:
        c[j] = None

for j in [1, 2, 3, 4]:
    if c[j] is None:
        raise ValueError(f'Parameter c_{j} not provided in model')

# Parameters
C = ['A', 'B', 'C', 'D', 'E']
J = [1, 2, 3, 4]

d = dict()
d['A'] = 1
d['B'] = 2
d['C'] = 3
d['D'] = 4
d['E'] = 8

cap = dict()
cap[1] = 2
cap[2] = 6
cap[3] = 8
cap[4] = 11

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x = dict()
for i in C:
    for j in J:
        x[i, j] = solver.BoolVar('x_' + i + '_' + str(j))

z = dict()
for j in J:
    z[j] = solver.BoolVar('z_' + str(j))

# Objective function
obj_expr = sum(c[j] * z[j] for j in J)
solver.Minimize(obj_expr)

# Customer service constraints: each customer served by exactly one truck
for i in C:
    solver.Add(sum(x[i, j] for j in J) == 1)

# Linking constraints: x_ij <= z_j
for i in C:
    for j in J:
        solver.Add(x[i, j] <= z[j])

# Truck capacity constraints
for j in J:
    solver.Add(sum(d[i] * x[i, j] for i in C) <= cap[j])

# Conflict constraints
for j in J:
    solver.Add(x['A', j] + x['C', j] <= 1)
    solver.Add(x['B', j] + x['D', j] <= 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")