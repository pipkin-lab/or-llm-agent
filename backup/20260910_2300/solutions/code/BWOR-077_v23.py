from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Define index sets
workers = ['A', 'B', 'C', 'D', 'E']
stations = ['I', 'II', 'III', 'IV', 'V']

# Efficiency parameters e[w][s]
efficiency = dict()
efficiency['A'] = dict()
efficiency['A']['I'] = 2
efficiency['A']['II'] = 3
efficiency['A']['III'] = 4
efficiency['A']['IV'] = 1
efficiency['A']['V'] = 7
efficiency['B'] = dict()
efficiency['B']['I'] = 3
efficiency['B']['II'] = 4
efficiency['B']['III'] = 2
efficiency['B']['IV'] = 5
efficiency['B']['V'] = 6
efficiency['C'] = dict()
efficiency['C']['I'] = 2
efficiency['C']['II'] = 5
efficiency['C']['III'] = 3
efficiency['C']['IV'] = 4
efficiency['C']['V'] = 1
efficiency['D'] = dict()
efficiency['D']['I'] = 5
efficiency['D']['II'] = 2
efficiency['D']['III'] = 3
efficiency['D']['IV'] = 2
efficiency['D']['V'] = 5
efficiency['E'] = dict()
efficiency['E']['I'] = 3
efficiency['E']['II'] = 7
efficiency['E']['III'] = 6
efficiency['E']['IV'] = 2
efficiency['E']['V'] = 4

# Decision variables
# x[w][s] is 1 if worker w is assigned to station s
x = dict()
for w in workers:
    x[w] = dict()
    for s in stations:
        x[w][s] = solver.BoolVar('x_' + w + '_' + s)

# Z: overall production capacity (bottleneck rate)
Z = solver.NumVar(0, solver.infinity(), 'Z')

# Objective: maximize Z
solver.Maximize(Z)

# Constraint 1: Each worker is assigned to exactly one station
for w in workers:
    solver.Add(sum(x[w][s] for s in stations) == 1)

# Constraint 2: Each station is assigned exactly one worker
for s in stations:
    solver.Add(sum(x[w][s] for w in workers) == 1)

# Constraint 3: Bottleneck constraints
for s in stations:
    solver.Add(sum(efficiency[w][s] * x[w][s] for w in workers) >= Z)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")