from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

G = ['A', 'B', 'C', 'D', 'E']
K = [1, 2, 3, 4, 5]

n = dict()
n['A'] = 5000
n['B'] = 12500
n['C'] = 15000
n['D'] = 10000
n['E'] = 7500

x = dict()
for g in G:
    for k in K:
        x[g, k] = solver.BoolVar('x_' + g + '_' + str(k))

# Assignment constraints: each grade to exactly one step
for g in G:
    solver.Add(sum(x[g, k] for k in K) == 1)

# Assignment constraints: each step to exactly one grade
for k in K:
    solver.Add(sum(x[g, k] for g in G) == 1)

# Objective: Minimize sum over k of k * sum over g of n_g * x_{g,k}
obj = 0
for g in G:
    for k in K:
        obj += k * n[g] * x[g, k]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")