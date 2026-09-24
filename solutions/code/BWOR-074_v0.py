from ortools.linear_solver import pywraplp

# Model Type: MILP
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
G = ['A', 'B', 'C', 'D', 'E']
K = [1, 2, 3, 4, 5]

# Parameters
N = 50000
n_g = dict()
n_g['A'] = 5000
n_g['B'] = 12500
n_g['C'] = 15000
n_g['D'] = 10000
n_g['E'] = 7500

# Decision Variables: x[g, k] = 1 if grade g is sorted at position k
x = dict()
for g in G:
    for k in K:
        x[g, k] = solver.BoolVar('x_' + g + '_' + str(k))

# Constraints:
# 1. Each grade is assigned to exactly one position
for g in G:
    solver.Add(sum(x[g, k] for k in K) == 1)

# 2. Each position is assigned exactly one grade
for k in K:
    solver.Add(sum(x[g, k] for g in G) == 1)

# Objective: Minimize W = 5*N - sum_j sum_g n_g * (5 - j) * x[g, j]
# Equivalently: Maximize sum_j sum_g n_g * (5 - j) * x[g, j]
# Since 5*N is constant, minimizing W is equivalent to maximizing the subtracted term.
# We'll minimize W directly.

# W = sum_{k=1}^{5} (N - s_k) where s_k = sum_{j=1}^{k-1} sum_{g'} n_{g'} * x_{g',j}
# But the linearized form is: W = 5*N - sum_{j=1}^{5} sum_{g} n_g * (5 - j) * x_{g,j}

obj_terms = []
for j in K:
    for g in G:
        coeff = n_g[g] * (5 - j)
        obj_terms.append(coeff * x[g, j])

# We want to MINIMIZE W = 5*N - sum(obj_terms)
# So we MINIMIZE (5*N - sum(obj_terms)) which is equivalent to MAXIMIZING sum(obj_terms)
# Let's use Maximize on the subtracted term to keep numbers positive, or just Minimize the full expression.
# Let's stick to the model's boxed formula: min W = 5N - sum(...)
# To avoid negative coefficients in minimization (which is fine for LP/MILP), 
# let's just build the expression.

# Expression to minimize: 5*N - sum_{j,g} n_g * (5-j) * x[g,j]
# This is: constant - linear_expression
# In OR-Tools, we can just do: solver.Minimize(5*N - sum(...))
# Or equivalently solver.Maximize(sum(...))

# Let's use Maximize for the sum term, then calculate final W.
max_expr = sum(obj_terms)
solver.Maximize(max_expr)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # The objective value from solver is the MAX value of sum(n_g * (5-j) * x[g,j])
    max_val = solver.Objective().Value()
    # The actual workload W = 5*N - max_val
    W = 5 * N - max_val
    print("OPTIMAL_VALUE:", W)
else:
    print("NO_FEASIBLE_SOLUTION")