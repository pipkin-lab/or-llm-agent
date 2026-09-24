from ortools.linear_solver import pywraplp

# Cost matrix c[i][j], 1-indexed
c = dict()
costs = {
    1: [4, 8, 7, 15, 12],
    2: [7, 9, 17, 14, 10],
    3: [6, 9, 12, 8, 7],
    4: [6, 7, 14, 6, 10],
    5: [6, 9, 12, 10, 6]
}
for i in range(1, 6):
    for j in range(1, 6):
        c[i, j] = costs[i][j - 1]

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[i, j]
x = dict()
for i in range(1, 6):
    for j in range(1, 6):
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: minimize total cost
obj = 0
for i in range(1, 6):
    for j in range(1, 6):
        obj += c[i, j] * x[i, j]
solver.Minimize(obj)

# Constraint: each store assigned to exactly one company
for j in range(1, 6):
    solver.Add(sum(x[i, j] for i in range(1, 6)) == 1)

# Constraint: each company assigned to at most one store
for i in range(1, 6):
    solver.Add(sum(x[i, j] for j in range(1, 6)) <= 1)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")