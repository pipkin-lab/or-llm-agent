from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
C = dict()
C[1, 1] = 0.8
C[1, 2] = 2.0
C[1, 3] = 3.8
C[1, 4] = 6.0
C[2, 1] = 0.9
C[2, 2] = 2.1
C[2, 3] = 3.9
C[3, 1] = 1.1
C[3, 2] = 2.3
C[4, 1] = 1.4

# Variables
x = dict()
for t in range(1, 5):
    for k in range(1, 5 - t + 1):
        x[t, k] = solver.NumVar(0, 1, 'x_' + str(t) + '_' + str(k))

# Objective
obj = sum(C[t, k] * x[t, k] for t in range(1, 5) for k in range(1, 5 - t + 1))
solver.Minimize(obj)

# Constraints: coverage for each year
# Year 1
solver.Add(x[1, 1] + x[1, 2] + x[1, 3] + x[1, 4] == 1)
# Year 2
solver.Add(x[1, 2] + x[1, 3] + x[1, 4] + x[2, 1] + x[2, 2] + x[2, 3] == 1)
# Year 3
solver.Add(x[1, 3] + x[1, 4] + x[2, 2] + x[2, 3] + x[3, 1] + x[3, 2] == 1)
# Year 4
solver.Add(x[1, 4] + x[2, 3] + x[3, 2] + x[4, 1] == 1)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")