from ortools.linear_solver import pywraplp

# Data
workers = ['A', 'B', 'C', 'D', 'E']
stations = ['I', 'II', 'III', 'IV', 'V']

c = dict()
efficiency = {
    'A': {'I': 2, 'II': 3, 'III': 4, 'IV': 1, 'V': 7},
    'B': {'I': 3, 'II': 4, 'III': 2, 'IV': 5, 'V': 6},
    'C': {'I': 2, 'II': 5, 'III': 3, 'IV': 4, 'V': 1},
    'D': {'I': 5, 'II': 2, 'III': 3, 'IV': 2, 'V': 5},
    'E': {'I': 3, 'II': 7, 'III': 6, 'IV': 2, 'V': 4}
}

for i in workers:
    for j in stations:
        c[i, j] = efficiency[i][j]

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x = dict()
for i in workers:
    for j in stations:
        x[i, j] = solver.BoolVar('x_' + i + '_' + j)

# Objective: Maximize total efficiency
objective = 0
for i in workers:
    for j in stations:
        objective += c[i, j] * x[i, j]

solver.Maximize(objective)

# Constraints: Each worker assigned to exactly one station
for i in workers:
    solver.Add(sum(x[i, j] for j in stations) == 1)

# Constraints: Each station staffed by exactly one worker
for j in stations:
    solver.Add(sum(x[i, j] for i in workers) == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")