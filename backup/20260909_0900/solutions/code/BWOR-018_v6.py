from ortools.linear_solver import pywraplp

# Define the cost matrix
c = [
    [4, 8, 7, 15, 12],
    [7, 9, 17, 14, 10],
    [6, 9, 12, 8, 7],
    [6, 7, 14, 6, 10],
    [6, 9, 12, 10, 6]
]

n = 5

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Create variables
x = dict()
for i in range(n):
    for j in range(n):
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Add constraints
# Each store is built by exactly one company
for j in range(n):
    solver.Add(sum(x[i, j] for i in range(n)) == 1)

# Each company is assigned to exactly one store
for i in range(n):
    solver.Add(sum(x[i, j] for j in range(n)) == 1)

# Objective function
obj = sum(c[i][j] * x[i, j] for i in range(n) for j in range(n))
solver.Minimize(obj)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")