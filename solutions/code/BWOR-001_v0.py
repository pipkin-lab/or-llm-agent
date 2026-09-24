from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets
materials = ['A', 'B', 'C']
brands = ['X', 'Y', 'Z']

# Parameters
c = dict()
c['A'] = 2.00
c['B'] = 1.50
c['C'] = 1.00

U = dict()
U['A'] = 2000
U['B'] = 2500
U['C'] = 1200

p = dict()
p['X'] = 0.50
p['Y'] = 0.40
p['Z'] = 0.30

s = dict()
s['X'] = 3.40
s['Y'] = 2.85
s['Z'] = 2.25

# Decision variables m[i][j]: amount of material i used in brand j
m = dict()
for i in materials:
    for j in brands:
        m[i, j] = solver.NumVar(0, INF, 'm_' + i + '_' + j)

# Objective function: Maximize Profit
# Profit = sum over j of (s_j - p_j) * total_j - sum over i of c_i * total_i
# Equivalent to sum over i,j of (s_j - p_j - c_i) * m[i,j]
obj = 0
for i in materials:
    for j in brands:
        coeff = s[j] - p[j] - c[i]
        obj += coeff * m[i, j]

solver.Maximize(obj)

# Composition Constraints

# Brand X: A >= 60%, C <= 20%
# A >= 60%: m['A','X'] >= 0.60*(m['A','X'] + m['B','X'] + m['C','X'])
# => 0.40*m['A','X'] - 0.60*m['B','X'] - 0.60*m['C','X'] >= 0
solver.Add(0.40 * m['A', 'X'] - 0.60 * m['B', 'X'] - 0.60 * m['C', 'X'] >= 0)

# C <= 20%: m['C','X'] <= 0.20*(m['A','X'] + m['B','X'] + m['C','X'])
# => -0.20*m['A','X'] - 0.20*m['B','X'] + 0.80*m['C','X'] <= 0
solver.Add(-0.20 * m['A', 'X'] - 0.20 * m['B', 'X'] + 0.80 * m['C', 'X'] <= 0)

# Brand Y: A >= 30%, C <= 50%
# A >= 30%: m['A','Y'] >= 0.30*(m['A','Y'] + m['B','Y'] + m['C','Y'])
# => 0.70*m['A','Y'] - 0.30*m['B','Y'] - 0.30*m['C','Y'] >= 0
solver.Add(0.70 * m['A', 'Y'] - 0.30 * m['B', 'Y'] - 0.30 * m['C', 'Y'] >= 0)

# C <= 50%: m['C','Y'] <= 0.50*(m['A','Y'] + m['B','Y'] + m['C','Y'])
# => -0.50*m['A','Y'] - 0.50*m['B','Y'] + 0.50*m['C','Y'] <= 0
solver.Add(-0.50 * m['A', 'Y'] - 0.50 * m['B', 'Y'] + 0.50 * m['C', 'Y'] <= 0)

# Brand Z: C <= 60%
# C <= 60%: m['C','Z'] <= 0.60*(m['A','Z'] + m['B','Z'] + m['C','Z'])
# => -0.60*m['A','Z'] - 0.60*m['B','Z'] + 0.40*m['C','Z'] <= 0
solver.Add(-0.60 * m['A', 'Z'] - 0.60 * m['B', 'Z'] + 0.40 * m['C', 'Z'] <= 0)

# Resource Availability Constraints
# Material A
solver.Add(m['A', 'X'] + m['A', 'Y'] + m['A', 'Z'] <= U['A'])

# Material B
solver.Add(m['B', 'X'] + m['B', 'Y'] + m['B', 'Z'] <= U['B'])

# Material C
solver.Add(m['C', 'X'] + m['C', 'Y'] + m['C', 'Z'] <= U['C'])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")