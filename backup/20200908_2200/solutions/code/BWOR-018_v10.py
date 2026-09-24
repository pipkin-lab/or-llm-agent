from ortools.linear_solver import pywraplp

# Define the problem
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
I = range(5)  # Companies 1-5
J = range(5)  # Stores 1-5

# Cost matrix c[i][j]
c = [
    [4, 8, 7, 15, 12],
    [7, 9, 17, 14, 10],
    [6, 9, 12, 8, 7],
    [6, 7, 14, 6, 10],
    [6, 9, 12, 10, 6]
]

# Decision variables: x[i][j] is binary
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective function: minimize total cost
obj = 0
for i in I:
    for j in J:
        obj += c[i][j] * x[i, j]
solver.Minimize(obj)

# Constraint 1: Each store is built by exactly one company
for j in J:
    constraint = sum(x[i, j] for i in I)
    solver.Add(constraint == 1)

# Constraint 2: Each company is assigned to at most one store
for i in I:
    constraint = sum(x[i, j] for j in J)
    solver.Add(constraint <= 1)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")