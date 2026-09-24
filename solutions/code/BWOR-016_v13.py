from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Define index sets
I_old = ['A1', 'A2']
I_new = ['A3', 'A4']
I = I_old + I_new
J = ['B1', 'B2', 'B3', 'B4']

# Parameters
cap = dict()
cap['A1'] = 400
cap['A2'] = 600
cap['A3'] = 200
cap['A4'] = 200

d = dict()
d['B1'] = 350
d['B2'] = 400
d['B3'] = 300
d['B4'] = 150

c = dict()
# c[i][j] = cost from i to j
for i in I:
    c[i] = dict()
for i, j in [('A1','B1'),('A1','B2'),('A1','B3'),('A1','B4'),
             ('A2','B1'),('A2','B2'),('A2','B3'),('A2','B4'),
             ('A3','B1'),('A3','B2'),('A3','B3'),('A3','B4'),
             ('A4','B1'),('A4','B2'),('A4','B3'),('A4','B4')]:
    pass

c['A1']['B1'] = 2
c['A1']['B2'] = 9
c['A1']['B3'] = 3
c['A1']['B4'] = 4
c['A2']['B1'] = 8
c['A2']['B2'] = 3
c['A2']['B3'] = 5
c['A2']['B4'] = 7
c['A3']['B1'] = 7
c['A3']['B2'] = 6
c['A3']['B3'] = 1
c['A3']['B4'] = 2
c['A4']['B1'] = 4
c['A4']['B2'] = 5
c['A4']['B3'] = 2
c['A4']['B4'] = 5

f = dict()
f['A3'] = 1200
f['A4'] = 1500

# Decision variables
# y_i for new factories (binary)
y = dict()
for i in I_new:
    y[i] = solver.BoolVar('y_' + i)

# x_ij for all factories and demand locations (continuous)
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# Objective function: Minimize Z
obj = 0
for i in I_new:
    obj += f[i] * y[i]
for i in I:
    for j in J:
        obj += c[i][j] * x[i, j]

solver.Minimize(obj)

# Constraint 1: Exactly one new factory built
solver.Add(y['A3'] + y['A4'] == 1)

# Constraint 2: Supply capacity constraints
for i in I_old:
    solver.Add(sum(x[i, j] for j in J) <= cap[i])

for i in I_new:
    solver.Add(sum(x[i, j] for j in J) <= cap[i] * y[i])

# Constraint 3: Demand satisfaction constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) == d[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")