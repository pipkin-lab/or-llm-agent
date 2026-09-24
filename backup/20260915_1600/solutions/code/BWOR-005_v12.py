from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index sets
C = ['A', 'B', 'C']
K = ['F', 'M', 'R']

# Parameters
W_max = dict()
W_max['F'] = 2000
W_max['M'] = 3000
W_max['R'] = 1500

V_max = dict()
V_max['F'] = 4000
V_max['M'] = 5000
V_max['R'] = 1500

Q = dict()
Q['A'] = 600
Q['B'] = 1000
Q['C'] = 800

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

# Decision variables
x = dict()
for c in C:
    for k in K:
        x[c, k] = solver.IntVar(0, INF, 'x_' + c + '_' + k)

# Objective: Maximize total revenue
obj = 0
for c in C:
    for k in K:
        obj += r[c] * x[c, k]
solver.Maximize(obj)

# A. Volume Constraints
for k in K:
    expr = sum(v[c] * x[c, k] for c in C)
    solver.Add(expr <= V_max[k])

# B. Weight Constraints (Capacity)
for k in K:
    expr = sum(w[c] * x[c, k] for c in C)
    solver.Add(expr <= W_max[k])

# C. Cargo Availability Constraints
for c in C:
    expr = sum(x[c, k] for k in K)
    solver.Add(expr <= Q[c])

# D. Maritime Safety / Balance Constraints
# Define weight expressions for each compartment
WF = sum(w[c] * x[c, 'F'] for c in C)
WM = sum(w[c] * x[c, 'M'] for c in C)
WR = sum(w[c] * x[c, 'R'] for c in C)

# 1. Front vs Middle: 30*WF - 23*WM <= 0 and 30*WF - 17*WM >= 0
solver.Add(30 * WF - 23 * WM <= 0)
solver.Add(30 * WF - 17 * WM >= 0)

# 2. Rear vs Middle: 40*WR - 23*WM <= 0 and 40*WR - 17*WM >= 0
solver.Add(40 * WR - 23 * WM <= 0)
solver.Add(40 * WR - 17 * WM >= 0)

# 3. Front vs Rear: 15*WF - 22*WR <= 0 and 15*WF - 18*WR >= 0
solver.Add(15 * WF - 22 * WR <= 0)
solver.Add(15 * WF - 18 * WR >= 0)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")