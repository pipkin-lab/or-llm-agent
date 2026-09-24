from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

P = [1, 2, 3]
T = [1, 2, 3, 4]

d = dict()
d[1, 1] = 1500
d[1, 2] = 1000
d[1, 3] = 2000
d[1, 4] = 1200
d[2, 1] = 1500
d[2, 2] = 1500
d[2, 3] = 1200
d[2, 4] = 1500
d[3, 1] = 1000
d[3, 2] = 2000
d[3, 3] = 1500
d[3, 4] = 2500

H = dict()
for t in T:
    H[t] = 15000

h = dict()
h[1] = 2
h[2] = 4
h[3] = 3

L_penalty = dict()
L_penalty[1] = 20
L_penalty[2] = 20
L_penalty[3] = 10

I_c = 5

x = dict()
S = dict()
L = dict()

for p in P:
    for t in T:
        x[p, t] = solver.NumVar(0, INF, 'x_' + str(p) + '_' + str(t))
        S[p, t] = solver.NumVar(0, INF, 'S_' + str(p) + '_' + str(t))
        L[p, t] = solver.NumVar(0, INF, 'L_' + str(p) + '_' + str(t))

for p in P:
    for t in T:
        if t == 1:
            solver.Add(S[p, t] == x[p, t] - d[p, t] - L[p, t])
        else:
            solver.Add(S[p, t] == S[p, t - 1] + x[p, t] - d[p, t] + L[p, t - 1] - L[p, t])

for t in T:
    solver.Add(h[1] * x[1, t] + h[2] * x[2, t] + h[3] * x[3, t] <= H[t])

x[1, 2].SetUB(0)

for p in P:
    solver.Add(S[p, 4] == 150)
    solver.Add(L[p, 4] == 0)

obj = 0
for t in T:
    for p in P:
        obj += I_c * S[p, t]
        obj += L_penalty[p] * L[p, t]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")