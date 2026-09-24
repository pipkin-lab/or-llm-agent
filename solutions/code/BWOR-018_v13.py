from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

I = [1, 2, 3, 4, 5]
J = [1, 2, 3, 4, 5]

c = dict()
c[1, 1] = 4
c[1, 2] = 8
c[1, 3] = 7
c[1, 4] = 15
c[1, 5] = 12
c[2, 1] = 7
c[2, 2] = 9
c[2, 3] = 17
c[2, 4] = 14
c[2, 5] = 10
c[3, 1] = 6
c[3, 2] = 9
c[3, 3] = 12
c[3, 4] = 8
c[3, 5] = 7
c[4, 1] = 6
c[4, 2] = 7
c[4, 3] = 14
c[4, 4] = 6
c[4, 5] = 10
c[5, 1] = 6
c[5, 2] = 9
c[5, 3] = 12
c[5, 4] = 10
c[5, 5] = 6

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.IntVar(0, 1, 'x_' + str(i) + '_' + str(j))

obj = 0
for i in I:
    for j in J:
        obj += c[i, j] * x[i, j]

solver.Minimize(obj)

for j in J:
    solver.Add(sum(x[i, j] for i in I) == 1)

for i in I:
    solver.Add(sum(x[i, j] for j in J) == 1)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")