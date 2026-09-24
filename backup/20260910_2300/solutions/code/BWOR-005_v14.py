from ortools.linear_solver import pywraplp

# Parameters
C = ['A', 'B', 'C']
K = ['F', 'M', 'R']

S = dict()
S['A'] = 600
S['B'] = 1000
S['C'] = 800

v = dict()
v['A'] = 10
v['B'] = 5
v['C'] = 7

w = dict()
w['A'] = 8
w['B'] = 6
w['C'] = 4

p = dict()
p['A'] = 1000
p['B'] = 700
p['C'] = 600

L = dict()
L['F'] = 2000
L['M'] = 3000
L['R'] = 1500

V = dict()
V['F'] = 4000
V['M'] = 5000
V['R'] = 1500

solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
x = dict()
for j in C:
    for k in K:
        x[j, k] = solver.NumVar(0, solver.infinity(), 'x_' + j + '_' + k)

# Objective: maximize total revenue
obj = 0
for j in C:
    for k in K:
        obj += p[j] * x[j, k]
solver.Maximize(obj)

# Cargo supply constraints
for j in C:
    solver.Add(sum(x[j, k] for k in K) <= S[j])

# Volume capacity constraints
for k in K:
    solver.Add(sum(v[j] * x[j, k] for j in C) <= V[k])

# Weight capacity constraints
for k in K:
    solver.Add(sum(w[j] * x[j, k] for j in C) <= L[k])

# Balance constraints
# Weight in each compartment
WF = sum(w[j] * x[j, 'F'] for j in C)
WM = sum(w[j] * x[j, 'M'] for j in C)
WR = sum(w[j] * x[j, 'R'] for j in C)

# a) Front/Middle ratio: (17/30) WM <= WF <= (23/30) WM
solver.Add(30 * WF - 23 * WM <= 0)
solver.Add(-30 * WF + 17 * WM <= 0)

# b) Rear/Middle ratio: (17/40) WM <= WR <= (23/40) WM
solver.Add(40 * WR - 23 * WM <= 0)
solver.Add(-40 * WR + 17 * WM <= 0)

# c) Front/Rear ratio: (6/5) WR <= WF <= (22/15) WR
solver.Add(15 * WF - 22 * WR <= 0)
solver.Add(-15 * WF + 18 * WR <= 0)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")