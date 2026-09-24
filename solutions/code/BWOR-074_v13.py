from ortools.linear_solver import pywraplp

# Parameters
N = 50000
grades = ['A', 'B', 'C', 'D', 'E']
n = dict()
n['A'] = 5000
n['B'] = 12500
n['C'] = 15000
n['D'] = 10000
n['E'] = 7500

steps = [1, 2, 3, 4, 5]

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    raise RuntimeError("SCIP solver not available")

# Decision variables: x[g][k] = 1 if grade g is sorted at step k
x = dict()
for g in grades:
    for k in steps:
        x[(g, k)] = solver.BoolVar('x_' + g + '_' + str(k))

# Constraints
# 1. Each grade is sorted exactly once
for g in grades:
    solver.Add(sum(x[(g, k)] for k in steps) == 1)

# 2. Each step processes exactly one grade
for k in steps:
    solver.Add(sum(x[(g, k)] for g in grades) == 1)

# Objective: Minimize total workload
# W = sum_{k=1}^{5} (N - sum_{j=1}^{k-1} sum_{g} n_g * x[g][j])
# This is linear in x. Let's build it directly.
# Term for step k is: N - sum_{j < k} sum_{g} n_g * x[g][j]
# Total W = 5*N - sum_{k=1}^{5} sum_{j < k} sum_{g} n_g * x[g][j]
#          = 5*N - sum_{j=1}^{4} sum_{g} n_g * x[g][j] * (5 - j)
# Since 5*N is constant, minimizing W is equivalent to minimizing
# - sum_{j=1}^{4} sum_{g} n_g * (5 - j) * x[g][j]
# Or equivalently, maximizing sum_{j=1}^{5} sum_{g} n_g * (5 - j) * x[g][j]
# (note: for j=5, coefficient is 0, so it doesn't matter)

# Let's just build the full linear expression for W and minimize it.
# W = sum_{k=1}^{5} (N - sum_{j=1}^{k-1} sum_{g in G} n_g * x[g][j])
obj_terms = []
for k in steps:
    # remaining before step k = N - sum_{j < k} sum_g n_g * x[g][j]
    remaining_expr = N
    for j in steps:
        if j < k:
            for g in grades:
                remaining_expr -= n[g] * x[(g, j)]
    obj_terms.append(remaining_expr)

# Sum all remaining expressions
total_workload = sum(obj_terms)

# Minimize total workload
solver.Minimize(total_workload)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")