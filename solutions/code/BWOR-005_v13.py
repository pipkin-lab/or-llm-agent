from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

compartments = ['F', 'M', 'R']
cargos = ['A', 'B', 'C']

CapW = dict()
CapW['F'] = 2000
CapW['M'] = 3000
CapW['R'] = 1500

CapV = dict()
CapV['F'] = 4000
CapV['M'] = 5000
CapV['R'] = 1500

Qty = dict()
Qty['A'] = 600
Qty['B'] = 1000
Qty['C'] = 800

v = dict()
v['A'] = 10
v['B'] = 5
v['C'] = 7

w = dict()
w['A'] = 8
w['B'] = 6
w['C'] = 4

r = dict()
r['A'] = 1000
r['B'] = 700
r['C'] = 600

x = dict()
for i in compartments:
    for j in cargos:
        x[i, j] = solver.IntVar(0, INF, 'x_' + i + '_' + j)

# Cargo availability constraints
for j in cargos:
    solver.Add(sum(x[i, j] for i in compartments) <= Qty[j])

# Compartment volume constraints
for i in compartments:
    solver.Add(sum(v[j] * x[i, j] for j in cargos) <= CapV[i])

# Compartment weight constraints
for i in compartments:
    solver.Add(sum(w[j] * x[i, j] for j in cargos) <= CapW[i])

# Balance constraints
# 1. Front/Middle Lower: 45*W_F - 17*W_M >= 0
solver.Add(
    45 * (8 * x['F', 'A'] + 6 * x['F', 'B'] + 4 * x['F', 'C'])
    - 17 * (8 * x['M', 'A'] + 6 * x['M', 'B'] + 4 * x['M', 'C']) >= 0
)

# 2. Front/Middle Upper: 45*W_F - 23*W_M <= 0
solver.Add(
    45 * (8 * x['F', 'A'] + 6 * x['F', 'B'] + 4 * x['F', 'C'])
    - 23 * (8 * x['M', 'A'] + 6 * x['M', 'B'] + 4 * x['M', 'C']) <= 0
)

# 3. Rear/Middle Lower: 40*W_R - 17*W_M >= 0
solver.Add(
    40 * (8 * x['R', 'A'] + 6 * x['R', 'B'] + 4 * x['R', 'C'])
    - 17 * (8 * x['M', 'A'] + 6 * x['M', 'B'] + 4 * x['M', 'C']) >= 0
)

# 4. Rear/Middle Upper: 40*W_R - 23*W_M <= 0
solver.Add(
    40 * (8 * x['R', 'A'] + 6 * x['R', 'B'] + 4 * x['R', 'C'])
    - 23 * (8 * x['M', 'A'] + 6 * x['M', 'B'] + 4 * x['M', 'C']) <= 0
)

# 5. Front/Rear Lower: 5*W_F - 6*W_R >= 0
solver.Add(
    5 * (8 * x['F', 'A'] + 6 * x['F', 'B'] + 4 * x['F', 'C'])
    - 6 * (8 * x['R', 'A'] + 6 * x['R', 'B'] + 4 * x['R', 'C']) >= 0
)

# 6. Front/Rear Upper: 15*W_F - 22*W_R <= 0
solver.Add(
    15 * (8 * x['F', 'A'] + 6 * x['F', 'B'] + 4 * x['F', 'C'])
    - 22 * (8 * x['R', 'A'] + 6 * x['R', 'B'] + 4 * x['R', 'C']) <= 0
)

# Objective function: Maximize total revenue
obj = 0
for i in compartments:
    for j in cargos:
        obj += r[j] * x[i, j]

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")