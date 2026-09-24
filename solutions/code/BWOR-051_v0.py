from ortools.linear_solver import pywraplp

# Parameters
persons = ['X', 'Y', 'Z', 'R']
tasks = ['A', 'B', 'C', 'D', 'F']

c = dict()
c['X', 'A'] = 25
c['X', 'B'] = 29
c['X', 'C'] = 31
c['X', 'D'] = 42
c['X', 'F'] = 37
c['Y', 'A'] = 39
c['Y', 'B'] = 38
c['Y', 'C'] = 26
c['Y', 'D'] = 20
c['Y', 'F'] = 33
c['Z', 'A'] = 34
c['Z', 'B'] = 27
c['Z', 'C'] = 28
c['Z', 'D'] = 40
c['Z', 'F'] = 32
c['R', 'A'] = 24
c['R', 'B'] = 42
c['R', 'C'] = 36
c['R', 'D'] = 23
c['R', 'F'] = 45

results = dict()

# Scenario (a)
solver_a = pywraplp.Solver.CreateSolver('SCIP')
INF = solver_a.infinity()

x_a = dict()
for p in persons:
    for t in tasks:
        x_a[p, t] = solver_a.BoolVar('x_a_' + p + '_' + t)

y_a = dict()
for p in persons:
    y_a[p] = solver_a.BoolVar('y_a_' + p)

obj_a = sum(c[p, t] * x_a[p, t] for p in persons for t in tasks)
solver_a.Minimize(obj_a)

for t in tasks:
    solver_a.Add(sum(x_a[p, t] for p in persons) == 1)

solver_a.Add(sum(y_a[p] for p in persons) == 1)

for p in persons:
    solver_a.Add(sum(x_a[p, t] for t in tasks) == 1 + y_a[p])

status_a = solver_a.Solve()
if status_a == pywraplp.Solver.OPTIMAL or status_a == pywraplp.Solver.FEASIBLE:
    results['a'] = solver_a.Objective().Value()
else:
    results['a'] = None

# Scenario (b)
solver_b = pywraplp.Solver.CreateSolver('SCIP')
INF_b = solver_b.infinity()

x_b = dict()
for p in persons:
    for t in tasks:
        x_b[p, t] = solver_b.BoolVar('x_b_' + p + '_' + t)

obj_b = sum(c[p, t] * x_b[p, t] for p in persons for t in tasks)
solver_b.Minimize(obj_b)

for t in tasks:
    solver_b.Add(sum(x_b[p, t] for p in persons) == 1)

solver_b.Add(sum(x_b['Y', t] for t in tasks) == 1)
solver_b.Add(sum(x_b['R', t] for t in tasks) == 1)

solver_b.Add(sum(x_b['X', t] for t in tasks) + sum(x_b['Z', t] for t in tasks) == 3)
solver_b.Add(sum(x_b['X', t] for t in tasks) >= 1)
solver_b.Add(sum(x_b['X', t] for t in tasks) <= 2)
solver_b.Add(sum(x_b['Z', t] for t in tasks) >= 1)
solver_b.Add(sum(x_b['Z', t] for t in tasks) <= 2)

status_b = solver_b.Solve()
if status_b == pywraplp.Solver.OPTIMAL or status_b == pywraplp.Solver.FEASIBLE:
    results['b'] = solver_b.Objective().Value()
else:
    results['b'] = None

# Scenario (c)
solver_c = pywraplp.Solver.CreateSolver('SCIP')
INF_c = solver_c.infinity()

x_c = dict()
for p in persons:
    for t in tasks:
        x_c[p, t] = solver_c.BoolVar('x_c_' + p + '_' + t)

obj_c = sum(c[p, t] * x_c[p, t] for p in persons for t in tasks)
solver_c.Minimize(obj_c)

for p in persons:
    solver_c.Add(sum(x_c[p, t] for t in tasks) == 1)

solver_c.Add(sum(x_c[p, 'A'] for p in persons) == 1)
solver_c.Add(sum(x_c[p, 'B'] for p in persons) == 1)

solver_c.Add(sum(x_c[p, t] for p in persons for t in ['C', 'D', 'F']) == 2)

for t in ['C', 'D', 'F']:
    solver_c.Add(sum(x_c[p, t] for p in persons) <= 1)

status_c = solver_c.Solve()
if status_c == pywraplp.Solver.OPTIMAL or status_c == pywraplp.Solver.FEASIBLE:
    results['c'] = solver_c.Objective().Value()
else:
    results['c'] = None

print("OPTIMAL_VALUE:", results['a'], results['b'], results['c'])