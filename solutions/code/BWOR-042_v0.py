from ortools.linear_solver import pywraplp

# Data
I = [1, 2, 3]
J = [1, 2, 3, 4, 5]

s = dict()
s[1] = 50
s[2] = 100
s[3] = 150

d = dict()
d[1] = 25
d[2] = 115
d[3] = 60
d[4] = 30
d[5] = 70

c = dict()
c[1, 1] = 10
c[1, 2] = 15
c[1, 3] = 20
c[1, 4] = 20
c[1, 5] = 40
c[2, 1] = 20
c[2, 2] = 10
c[2, 3] = 15
c[2, 4] = 30
c[2, 5] = 30
c[3, 1] = 30
c[3, 2] = 35
c[3, 3] = 40
c[3, 4] = 55
c[3, 5] = 25

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

# Supply constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) == s[i])

# Demand constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) == d[j])

# Objective: minimize total cost
obj = sum(c[i, j] * x[i, j] for i in I for j in J)
solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")