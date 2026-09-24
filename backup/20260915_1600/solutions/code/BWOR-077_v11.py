from ortools.linear_solver import pywraplp

# Index sets
W = ['A', 'B', 'C', 'D', 'E']
S = ['I', 'II', 'III', 'IV', 'V']

# Efficiency parameters E[w][s]
E = {
    'A': {'I': 2, 'II': 3, 'III': 4, 'IV': 1, 'V': 7},
    'B': {'I': 3, 'II': 4, 'III': 2, 'IV': 5, 'V': 6},
    'C': {'I': 2, 'II': 5, 'III': 3, 'IV': 4, 'V': 1},
    'D': {'I': 5, 'II': 2, 'III': 3, 'IV': 2, 'V': 5},
    'E': {'I': 3, 'II': 7, 'III': 6, 'IV': 2, 'V': 4},
}

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x = dict()
for w in W:
    for s in S:
        x[(w, s)] = solver.BoolVar('x_' + w + '_' + s)

Z = solver.NumVar(0, solver.infinity(), 'Z')

# Worker Assignment Constraints: each worker assigned to exactly one station
for w in W:
    solver.Add(sum(x[(w, s)] for s in S) == 1)

# Station Staffing Constraints: each station assigned exactly one worker
for s in S:
    solver.Add(sum(x[(w, s)] for w in W) == 1)

# Bottleneck Capacity Constraints: Z <= capacity of each station
for s in S:
    solver.Add(Z <= sum(E[w][s] * x[(w, s)] for w in W))

# Objective: Maximize Z
solver.Maximize(Z)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")