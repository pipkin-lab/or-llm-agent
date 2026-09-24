from ortools.linear_solver import pywraplp

# Define solver (LP since variables are continuous)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Index sets
P = ['A', 'B', 'C', 'D']
R = ['I', 'II', 'III', 'IV', 'V', 'VI']

# Parameters
S = dict()
S['A'] = 200
S['B'] = 300
S['C'] = 400
S['D'] = 100

D = dict()
D['I'] = 200
D['II'] = 150
D['III'] = 400
D['IV'] = 100
D['V'] = 150
D['VI'] = 150

# Net profit per kg: pi[p][r] = s_r - c_p - t_{p,r}
# We'll compute coefficients as 1000 * pi (Yuan per ton)
c = dict()
c['A'] = 1.2
c['B'] = 1.4
c['C'] = 1.1
c['D'] = 1.5

s = dict()
s['I'] = 2.0
s['II'] = 2.4
s['III'] = 1.8
s['IV'] = 2.2
s['V'] = 1.6
s['VI'] = 2.0

t = dict()
t[('A', 'I')] = 0.5
t[('A', 'II')] = 0.4
t[('A', 'III')] = 0.3
t[('A', 'IV')] = 0.4
t[('A', 'V')] = 0.3
t[('A', 'VI')] = 0.1
t[('B', 'I')] = 0.3
t[('B', 'II')] = 0.8
t[('B', 'III')] = 0.9
t[('B', 'IV')] = 0.5
t[('B', 'V')] = 0.6
t[('B', 'VI')] = 0.2
t[('C', 'I')] = 0.7
t[('C', 'II')] = 0.7
t[('C', 'III')] = 0.3
t[('C', 'IV')] = 0.7
t[('C', 'V')] = 0.4
t[('C', 'VI')] = 0.4
t[('D', 'I')] = 0.6
t[('D', 'II')] = 0.4
t[('D', 'III')] = 0.2
t[('D', 'IV')] = 0.6
t[('D', 'V')] = 0.5
t[('D', 'VI')] = 0.8

# Decision variables: x[p, r] in tons
x = dict()
for p in P:
    for r in R:
        x[p, r] = solver.NumVar(0, solver.infinity(), 'x_' + p + '_' + r)

# Objective: Maximize total profit in Yuan
obj = 0
for p in P:
    for r in R:
        pi = s[r] - c[p] - t[(p, r)]
        coeff = 1000 * pi  # Yuan per ton
        obj += coeff * x[p, r]

solver.Maximize(obj)

# Supply capacity constraints
for p in P:
    solver.Add(sum(x[p, r] for r in R) <= S[p])

# Demand constraints
# General regions: I, II, V, VI (<= demand)
for r in ['I', 'II', 'V', 'VI']:
    solver.Add(sum(x[p, r] for p in P) <= D[r])

# Region III: 100 <= sum <= 400
solver.Add(sum(x[p, 'III'] for p in P) >= 100)
solver.Add(sum(x[p, 'III'] for p in P) <= D['III'])

# Region IV: exactly 100
solver.Add(sum(x[p, 'IV'] for p in P) == D['IV'])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")