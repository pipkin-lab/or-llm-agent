from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
C = [
    [4, 8, 7, 15, 12],
    [7, 9, 17, 14, 10],
    [6, 9, 12, 8, 7],
    [6, 7, 14, 6, 10],
    [6, 9, 12, 10, 6]
]

I = range(5)
J = range(5)

# Decision variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: minimize total cost
obj = 0
for i in I:
    for j in J:
        obj += C[i][j] * x[i, j]

solver.Minimize(obj)

# Constraints: each store built by exactly one company
for j in J:
    solver.Add(sum(x[i, j] for i in I) == 1)

# Constraints: each company assigned to exactly one store
for i in I:
    solver.Add(sum(x[i, j] for j in J) == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")