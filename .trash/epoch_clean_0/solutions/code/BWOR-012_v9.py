from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

G = [1, 2, 3]
B = ['R', 'Y', 'Bl']

S = dict()
S[1] = 1500
S[2] = 2000
S[3] = 1000

c = dict()
c[1] = 6.0
c[2] = 4.5
c[3] = 3.0

p = dict()
p['R'] = 5.5
p['Y'] = 5.0
p['Bl'] = 4.8

u3 = dict()
u3['R'] = 0.10
u3['Y'] = 0.70
u3['Bl'] = 0.50

l1 = dict()
l1['R'] = 0.50
l1['Y'] = 0.20
l1['Bl'] = 0.10

L_R = 2000

x = dict()
for g in G:
    for b in B:
        x[g, b] = solver.NumVar(0, solver.infinity(), 'x_' + str(g) + '_' + b)

for g in G:
    solver.Add(sum(x[g, b] for b in B) <= S[g])

for b in B:
    Xb = sum(x[g, b] for g in G)
    solver.Add(x[3, b] <= u3[b] * Xb)
    solver.Add(x[1, b] >= l1[b] * Xb)

solver.Add(sum(x[g, 'R'] for g in G) >= L_R)

obj = 0
for g in G:
    for b in B:
        obj += (p[b] - c[g]) * x[g, b]

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")