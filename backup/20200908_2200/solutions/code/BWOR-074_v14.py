from ortools.linear_solver import pywraplp

# Parameters
N = 50000
grades = ['A', 'B', 'C', 'D', 'E']
N_g = {
    'A': 5000,
    'B': 12500,
    'C': 15000,
    'D': 10000,
    'E': 7500
}
positions = [1, 2, 3, 4, 5]

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Variables
# x[g, k] = 1 if grade g is assigned to position k
x = dict()
for g in grades:
    for k in positions:
        x[g, k] = solver.BoolVar('x_' + g + '_' + str(k))

# Objective: Minimize Total Workload Z
# Z = 5*N - sum_{g} sum_{k} (5-k) * N_g * x[g, k]
# To minimize Z, we maximize the sum of savings: sum (5-k) * N_g * x[g, k]
# Since we want to MINIMIZE workload, and Z = 5N - savings, minimizing Z is equivalent to maximizing savings.
# However, standard pywraplp Minimize works on the expression directly.
# Let's construct the expression for Z directly.
# Constant part: 5 * N
# Variable part: - sum (5-k) * N_g * x[g,k]

# Alternatively, we can just minimize the variable part with a negative sign or maximize the positive part.
# Let's maximize savings to be safe with standard solvers, then calculate Z.
# Or simply minimize: 5*N - (savings_term)
# In pywraplp, we can pass a linear expression to Minimize.

obj_terms = 0
for g in grades:
    for k in positions:
        coeff = (5 - k) * N_g[g]
        obj_terms -= coeff * x[g, k]  # Because we are minimizing, and the term is subtracted in Z

# The constant 5*N doesn't affect the optimization, but we include it for the final value if needed.
# For the objective function passed to the solver, only variable terms matter.
solver.Minimize(obj_terms + 5 * N)

# Constraints
# 1. Each grade is assigned to exactly one position
for g in grades:
    solver.Add(sum(x[g, k] for k in positions) == 1)

# 2. Each position is assigned exactly one grade
for k in positions:
    solver.Add(sum(x[g, k] for g in grades) == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")