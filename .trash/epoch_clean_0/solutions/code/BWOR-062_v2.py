from ortools.linear_solver import pywraplp

# Initialize the solver (MILP since we have binary variables)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
R = [1, 2, 3]
K = [0, 1, 2, 3, 4]

# Profit data
profit = {
    (1, 0): 0, (1, 1): 16, (1, 2): 25, (1, 3): 30, (1, 4): 32,
    (2, 0): 0, (2, 1): 12, (2, 2): 17, (2, 3): 21, (2, 4): 22,
    (3, 0): 0, (3, 1): 10, (3, 2): 14, (3, 3): 16, (3, 4): 17,
}

M = 4  # Total number of sales outlets

# Decision variables
x = dict()
for r in R:
    for k in K:
        x[r, k] = solver.BoolVar('x_' + str(r) + '_' + str(k))

# Objective function: Maximize total profit
obj = sum(profit[r, k] * x[r, k] for r in R for k in K)
solver.Maximize(obj)

# Constraint A: Each region must be assigned exactly one number of outlets
for r in R:
    solver.Add(sum(x[r, k] for k in K) == 1)

# Constraint B: Total number of outlets allocated must equal M
solver.Add(sum(k * x[r, k] for r in R for k in K) == M)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")