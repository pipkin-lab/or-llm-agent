from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

I = [1, 2, 3]
J = [1, 2, 3]

S = dict()
S[1] = 20
S[2] = 30
S[3] = 20

D = dict()
D[1] = 15
D[2] = 25
D[3] = 20

c = dict()
c[1, 1] = 3
c[1, 2] = 10
c[1, 3] = 2
c[2, 1] = 4
c[2, 2] = 11
c[2, 3] = 8
c[3, 1] = 8
c[3, 2] = 11
c[3, 3] = 4

p = dict()
p[1] = 12
p[2] = 16
p[3] = 11

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

obj = 0
for i in I:
    for j in J:
        obj += (p[j] - c[i, j]) * x[i, j]

solver.Maximize(obj)

for i in I:
    solver.Add(sum(x[i, j] for j in J) <= S[i])

for j in J:
    solver.Add(sum(x[i, j] for i in I) <= D[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")