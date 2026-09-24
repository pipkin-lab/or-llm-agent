from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables x[i, j] for 1 <= i <= j <= 4
x = dict()
for i in range(1, 5):
    for j in range(i, 5):
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Pre-computed costs C[i, j]
C = dict()
C[1, 1] = 0.8
C[1, 2] = 2.0
C[1, 3] = 3.8
C[1, 4] = 6.0
C[2, 2] = 0.9
C[2, 3] = 2.1
C[2, 4] = 3.9
C[3, 3] = 1.1
C[3, 4] = 2.3
C[4, 4] = 1.4

# Objective: Minimize total cost
obj = 0
for i in range(1, 5):
    for j in range(i, 5):
        obj += C[i, j] * x[i, j]
solver.Minimize(obj)

# Coverage constraints for each year k
for k in range(1, 5):
    expr = 0
    for i in range(1, k + 1):
        for j in range(k, 5):
            expr += x[i, j]
    solver.Add(expr == 1)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")