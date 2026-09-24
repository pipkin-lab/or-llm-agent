from ortools.linear_solver import pywraplp

J = [1, 2, 3]
K = [1, 2, 3]

r = dict()
r[1, 1] = 0.3
r[2, 1] = 0.2
r[3, 1] = 0.1
r[1, 2] = 0.4
r[2, 2] = 0.5
r[3, 2] = 0.2
r[1, 3] = 0.5
r[2, 3] = 0.9
r[3, 3] = 0.7

c = dict()
c[1, 1] = 1
c[2, 1] = 3
c[3, 1] = 2
c[1, 2] = 2
c[2, 2] = 5
c[3, 2] = 3
c[1, 3] = 3
c[2, 3] = 6
c[3, 3] = 4

B = 8

solver = pywraplp.Solver.CreateSolver('SCIP')

x = dict()
for j in J:
    for k in K:
        x[j, k] = solver.BoolVar('x_' + str(j) + '_' + str(k))

for j in J:
    solver.Add(sum(x[j, k] for k in K) == 1)

solver.Add(sum(c[j, k] * x[j, k] for j in J for k in K) <= B)

obj = sum(r[j, k] * x[j, k] for j in J for k in K)
solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")