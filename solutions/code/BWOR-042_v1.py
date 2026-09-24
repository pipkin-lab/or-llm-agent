from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

I = [1, 2, 3]
J = ['A', 'B', 'C', 'D', 'E']

S = dict()
S[1] = 50
S[2] = 100
S[3] = 150

D = dict()
D['A'] = 25
D['B'] = 115
D['C'] = 60
D['D'] = 30
D['E'] = 70

c = dict()
c[1, 'A'] = 10
c[1, 'B'] = 15
c[1, 'C'] = 20
c[1, 'D'] = 20
c[1, 'E'] = 40
c[2, 'A'] = 20
c[2, 'B'] = 10
c[2, 'C'] = 15
c[2, 'D'] = 30
c[2, 'E'] = 30
c[3, 'A'] = 30
c[3, 'B'] = 35
c[3, 'C'] = 40
c[3, 'D'] = 55
c[3, 'E'] = 25

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + j)

obj = 0
for i in I:
    for j in J:
        obj += c[i, j] * x[i, j]

solver.Minimize(obj)

for i in I:
    solver.Add(sum(x[i, j] for j in J) == S[i])

for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")