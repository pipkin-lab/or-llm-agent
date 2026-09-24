from ortools.linear_solver import pywraplp

# Parameters
G = ['A', 'B', 'C', 'D', 'E']
P = [1, 2, 3, 4, 5]
N = 50000
n = dict()
n['A'] = 5000
n['B'] = 12500
n['C'] = 15000
n['D'] = 10000
n['E'] = 7500

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[g][k]
x = dict()
for g in G:
    for k in P:
        x[(g, k)] = solver.BoolVar('x_' + g + '_' + str(k))

# Constraints: each position gets exactly one grade
for k in P:
    solver.Add(sum(x[(g, k)] for g in G) == 1)

# Constraints: each grade assigned to exactly one position
for g in G:
    solver.Add(sum(x[(g, k)] for k in P) == 1)

# Objective: minimize Z = 5*N - sum_{k=1}^{4} (5-k) * sum_{g} n_g * x_{g,k}
# Equivalent to maximizing sum_{k=1}^{4} (5-k) * sum_g n_g * x_{g,k}
# We minimize the negative of that, i.e., minimize -(weighted sum)
# Or simply: minimize (5*N - weighted_sum) = 5*N + sum_{k=1}^{4} (k-5) * sum_g n_g * x_{g,k}
# Let's just build the full linear expression for Z.

obj = 5 * N
for k in P:
    if k <= 4:
        for g in G:
            obj += (k - 5) * n[g] * x[(g, k)]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")