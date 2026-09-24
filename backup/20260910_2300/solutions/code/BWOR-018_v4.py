from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

I = [0, 1, 2, 3, 4]
J = [0, 1, 2, 3, 4]

C = dict()
C[0, 0] = 4; C[0, 1] = 8; C[0, 2] = 7; C[0, 3] = 15; C[0, 4] = 12
C[1, 0] = 7; C[1, 1] = 9; C[1, 2] = 17; C[1, 3] = 14; C[1, 4] = 10
C[2, 0] = 6; C[2, 1] = 9; C[2, 2] = 12; C[2, 3] = 8; C[2, 4] = 7
C[3, 0] = 6; C[3, 1] = 7; C[3, 2] = 14; C[3, 3] = 6; C[3, 4] = 10
C[4, 0] = 6; C[4, 1] = 9; C[4, 2] = 12; C[4, 3] = 10; C[4, 4] = 6

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

obj = sum(C[i, j] * x[i, j] for i in I for j in J)

for j in J:
    solver.Add(sum(x[i, j] for i in I) == 1)

for i in I:
    solver.Add(sum(x[i, j] for j in J) == 1)

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")