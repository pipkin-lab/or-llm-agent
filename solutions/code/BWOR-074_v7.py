from ortools.linear_solver import pywraplp

# Parameters
N = 50000
grades = ['A', 'B', 'C', 'D', 'E']
proportions = {'A': 0.10, 'B': 0.25, 'C': 0.30, 'D': 0.20, 'E': 0.15}
n = dict()
for g in grades:
    n[g] = N * proportions[g]

steps = [1, 2, 3, 4, 5]

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables x[g, k] in {0, 1}
x = dict()
for g in grades:
    for k in steps:
        x[g, k] = solver.BoolVar('x_' + g + '_' + str(k))

# Constraints: each grade assigned to exactly one step
for g in grades:
    solver.Add(sum(x[g, k] for k in steps) == 1)

# Constraints: each step assigned exactly one grade
for k in steps:
    solver.Add(sum(x[g, k] for g in grades) == 1)

# Objective: minimize sum_{g} sum_{k} k * n[g] * x[g, k]
obj = sum(k * n[g] * x[g, k] for g in grades for k in steps)
solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")