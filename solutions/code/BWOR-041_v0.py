from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

I = ['A', 'B', 'C']
J = ['X', 'Y', 'Z']

supply = dict()
supply['A'] = 1000
supply['B'] = 2000
supply['C'] = 2000

demand = dict()
demand['X'] = 1500
demand['Y'] = 1500
demand['Z'] = 1500

c = dict()
c['A', 'X'] = 5
c['A', 'Y'] = 4
c['B', 'X'] = 16
c['B', 'Y'] = 8
c['B', 'Z'] = 6
c['C', 'X'] = 12
c['C', 'Y'] = 10
c['C', 'Z'] = 11

x = dict()
for i in I:
    for j in J:
        if i == 'A' and j == 'Z':
            continue
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# x_AZ = 0 is enforced by not creating the variable; we add an explicit constraint using 0.
# Since the variable doesn't exist, we simply note it's zero.

# Objective
obj_terms = []
for i in I:
    for j in J:
        if i == 'A' and j == 'Z':
            continue
        obj_terms.append(c[i, j] * x[i, j])
solver.Maximize(sum(obj_terms))

# Supply constraints (equality)
solver.Add(x['A', 'X'] + x['A', 'Y'] == supply['A'])
solver.Add(x['B', 'X'] + x['B', 'Y'] + x['B', 'Z'] == supply['B'])
solver.Add(x['C', 'X'] + x['C', 'Y'] + x['C', 'Z'] == supply['C'])

# Demand constraints (inequality)
for j in J:
    for i in I:
        if i == 'A' and j == 'Z':
            continue
        solver.Add(x[i, j] <= demand[j])

# Specific operational constraints
# x_AZ = 0 is already enforced by not creating the variable
# x_CZ >= 1000
solver.Add(x['C', 'Z'] >= 1000)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")