from ortools.linear_solver import pywraplp

# Parameters
G = ['A', 'B', 'C', 'D', 'E']
K = [1, 2, 3, 4, 5]
N = 50000

n_g = dict()
n_g['A'] = 5000
n_g['B'] = 12500
n_g['C'] = 15000
n_g['D'] = 10000
n_g['E'] = 7500

# Create solver (MILP - assignment problem)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[g, k]
x = dict()
for g in G:
    for k in K:
        x[g, k] = solver.BoolVar('x_' + g + '_' + str(k))

# Objective: Minimize sum over g in G, k in K of k * n_g * x[g, k]
obj = 0
for g in G:
    for k in K:
        obj += k * n_g[g] * x[g, k]

solver.Minimize(obj)

# Constraints: Each grade assigned to exactly one position
for g in G:
    solver.Add(sum(x[g, k] for k in K) == 1)

# Constraints: Each position assigned exactly one grade
for k in K:
    solver.Add(sum(x[g, k] for g in G) == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")