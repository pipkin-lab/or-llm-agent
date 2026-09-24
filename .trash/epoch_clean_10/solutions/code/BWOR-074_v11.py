from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Define sets and parameters
grades = ['A', 'B', 'C', 'D', 'E']
positions = [1, 2, 3, 4, 5]

n = {
    'A': 5000,
    'B': 12500,
    'C': 15000,
    'D': 10000,
    'E': 7500
}

# Define decision variables x[g][p]
x = dict()
for g in grades:
    for p in positions:
        x[g, p] = solver.BoolVar('x_' + g + '_' + str(p))

# Constraints: each grade assigned to exactly one position
for g in grades:
    solver.Add(sum(x[g, p] for p in positions) == 1)

# Constraints: each position assigned to exactly one grade
for p in positions:
    solver.Add(sum(x[g, p] for g in grades) == 1)

# Objective: minimize sum of n_g * p * x[g][p]
obj = sum(n[g] * p * x[g, p] for g in grades for p in positions)
solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")