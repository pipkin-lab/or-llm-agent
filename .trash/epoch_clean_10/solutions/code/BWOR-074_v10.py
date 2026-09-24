from ortools.linear_solver import pywraplp

# Define the problem
solver = pywraplp.Solver.CreateSolver('SCIP')

# Sets
grades = ['A', 'B', 'C', 'D', 'E']
num_grades = len(grades)
steps = range(1, 6)  # 1 to 5

# Parameters: number of sheets for each grade
n = {
    'A': 5000,
    'B': 12500,
    'C': 15000,
    'D': 10000,
    'E': 7500
}

# Weights: w_t = 5 - t
# t=1 -> 4, t=2 -> 3, t=3 -> 2, t=4 -> 1, t=5 -> 0
w = {t: 5 - t for t in steps}

# Decision Variables: x[k, t] = 1 if grade k is sorted at step t
x = dict()
for k in grades:
    for t in steps:
        x[k, t] = solver.BoolVar('x_' + k + '_' + str(t))

# Objective Function: Maximize sum of w_t * n_k * x[k, t]
objective_terms = []
for k in grades:
    for t in steps:
        objective_terms.append(w[t] * n[k] * x[k, t])

solver.Maximize(sum(objective_terms))

# Constraints
# 1. Each grade is assigned to exactly one step
for k in grades:
    solver.Add(sum(x[k, t] for t in steps) == 1)

# 2. Each step is assigned exactly one grade
for t in steps:
    solver.Add(sum(x[k, t] for k in grades) == 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # The solver maximizes the "savings" (weighted sum).
    # The actual minimum workload is Z_min = 5 * N - Savings
    # where N = 50000
    N = 50000
    savings = solver.Objective().Value()
    min_workload = 5 * N - savings
    print("OPTIMAL_VALUE:", min_workload)
else:
    print("NO_FEASIBLE_SOLUTION")