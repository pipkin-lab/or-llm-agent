from ortools.linear_solver import pywraplp

# Data
I = ['X', 'Y', 'Z', 'R']
J = ['A', 'B', 'C', 'D', 'F']

c = dict()
c[('X', 'A')] = 25
c[('X', 'B')] = 29
c[('X', 'C')] = 31
c[('X', 'D')] = 42
c[('X', 'F')] = 37
c[('Y', 'A')] = 39
c[('Y', 'B')] = 38
c[('Y', 'C')] = 26
c[('Y', 'D')] = 20
c[('Y', 'F')] = 33
c[('Z', 'A')] = 34
c[('Z', 'B')] = 27
c[('Z', 'C')] = 28
c[('Z', 'D')] = 40
c[('Z', 'F')] = 32
c[('R', 'A')] = 24
c[('R', 'B')] = 42
c[('R', 'C')] = 36
c[('R', 'D')] = 23
c[('R', 'F')] = 45

# Scenario A
solver_a = pywraplp.Solver.CreateSolver('SCIP')
x_a = dict()
for i in I:
    for j in J:
        x_a[(i, j)] = solver_a.BoolVar('x_a_' + i + '_' + j)

obj_a = sum(c[(i, j)] * x_a[(i, j)] for i in I for j in J)
solver_a.Minimize(obj_a)

for j in J:
    solver_a.Add(sum(x_a[(i, j)] for i in I) == 1)

for i in I:
    solver_a.Add(sum(x_a[(i, j)] for j in J) >= 1)
    solver_a.Add(sum(x_a[(i, j)] for j in J) <= 2)

status_a = solver_a.Solve()
if status_a == pywraplp.Solver.OPTIMAL or status_a == pywraplp.Solver.FEASIBLE:
    val_a = solver_a.Objective().Value()
else:
    val_a = None

# Scenario B
solver_b = pywraplp.Solver.CreateSolver('SCIP')
x_b = dict()
for i in I:
    for j in J:
        x_b[(i, j)] = solver_b.BoolVar('x_b_' + i + '_' + j)

obj_b = sum(c[(i, j)] * x_b[(i, j)] for i in I for j in J)
solver_b.Minimize(obj_b)

for j in J:
    solver_b.Add(sum(x_b[(i, j)] for i in I) == 1)

solver_b.Add(sum(x_b[('Y', j)] for j in J) == 1)
solver_b.Add(sum(x_b[('R', j)] for j in J) == 1)
solver_b.Add(sum(x_b[('X', j)] for j in J) >= 1)
solver_b.Add(sum(x_b[('X', j)] for j in J) <= 2)
solver_b.Add(sum(x_b[('Z', j)] for j in J) >= 1)
solver_b.Add(sum(x_b[('Z', j)] for j in J) <= 2)
solver_b.Add(sum(x_b[('X', j)] for j in J) + sum(x_b[('Z', j)] for j in J) == 3)

status_b = solver_b.Solve()
if status_b == pywraplp.Solver.OPTIMAL or status_b == pywraplp.Solver.FEASIBLE:
    val_b = solver_b.Objective().Value()
else:
    val_b = None

# Scenario C
solver_c = pywraplp.Solver.CreateSolver('SCIP')
x_c = dict()
for i in I:
    for j in J:
        x_c[(i, j)] = solver_c.BoolVar('x_c_' + i + '_' + j)

obj_c = sum(c[(i, j)] * x_c[(i, j)] for i in I for j in J)
solver_c.Minimize(obj_c)

for i in I:
    solver_c.Add(sum(x_c[(i, j)] for j in J) == 1)

solver_c.Add(sum(x_c[(i, 'A')] for i in I) == 1)
solver_c.Add(sum(x_c[(i, 'B')] for i in I) == 1)
solver_c.Add(sum(x_c[(i, j)] for i in I for j in ['C', 'D', 'F']) == 2)

status_c = solver_c.Solve()
if status_c == pywraplp.Solver.OPTIMAL or status_c == pywraplp.Solver.FEASIBLE:
    val_c = solver_c.Objective().Value()
else:
    val_c = None

# Output: combined result as sum of scenario optima (one representative value per scenario)
results = dict()
results['a'] = val_a
results['b'] = val_b
results['c'] = val_c

print("OPTIMAL_VALUE:", val_a, val_b, val_c)