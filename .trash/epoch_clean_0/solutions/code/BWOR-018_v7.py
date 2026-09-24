from ortools.linear_solver import pywraplp

# Define the number of companies and stores
n_companies = 5
n_stores = 5

# Cost matrix c[i][j]
c = [
    [4, 8, 7, 15, 12],
    [7, 9, 17, 14, 10],
    [6, 9, 12, 8, 7],
    [6, 7, 14, 6, 10],
    [6, 9, 12, 10, 6]
]

# Create the solver (MILP because variables are binary)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Create binary decision variables x[i][j]
x = dict()
for i in range(n_companies):
    for j in range(n_stores):
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective function: Minimize total cost
obj = 0
for i in range(n_companies):
    for j in range(n_stores):
        obj += c[i][j] * x[i, j]

solver.Minimize(obj)

# Constraint 1: Each store is built by exactly one company
for j in range(n_stores):
    solver.Add(sum(x[i, j] for i in range(n_companies)) == 1)

# Constraint 2: Each company is assigned to exactly one store
for i in range(n_companies):
    solver.Add(sum(x[i, j] for j in range(n_stores)) == 1)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")