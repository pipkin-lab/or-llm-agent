from ortools.linear_solver import pywraplp

I = ['A1', 'A2', 'A3', 'A4']
J = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']

s = dict()
s['A1'] = 50
s['A2'] = 40
s['A3'] = 60
s['A4'] = 31

d = dict()
d['B1'] = 30
d['B2'] = 50
d['B3'] = 20
d['B4'] = 40
d['B5'] = 30
d['B6'] = 11

c = dict()
c[('A1', 'B1')] = 2
c[('A1', 'B2')] = 1
c[('A1', 'B3')] = 3
c[('A1', 'B4')] = 3
c[('A1', 'B5')] = 3
c[('A1', 'B6')] = 5
c[('A2', 'B1')] = 4
c[('A2', 'B2')] = 2
c[('A2', 'B3')] = 2
c[('A2', 'B4')] = 4
c[('A2', 'B5')] = 4
c[('A2', 'B6')] = 4
c[('A3', 'B1')] = 3
c[('A3', 'B2')] = 5
c[('A3', 'B3')] = 4
c[('A3', 'B4')] = 2
c[('A3', 'B5')] = 4
c[('A3', 'B6')] = 1
c[('A4', 'B1')] = 4
c[('A4', 'B2')] = 2
c[('A4', 'B3')] = 2
c[('A4', 'B4')] = 1
c[('A4', 'B5')] = 2
c[('A4', 'B6')] = 2

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

obj = 0
for i in I:
    for j in J:
        obj += c[(i, j)] * x[i, j]

for i in I:
    solver.Add(sum(x[i, j] for j in J) == s[i])

for j in J:
    solver.Add(sum(x[i, j] for i in I) == d[j])

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")