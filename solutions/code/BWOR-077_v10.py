from ortools.linear_solver import pywraplp

# Define index sets
W = ['A', 'B', 'C', 'D', 'E']
S = ['I', 'II', 'III', 'IV', 'V']

# Efficiency matrix e[w][s]
e = dict()
e['A'] = dict()
e['B'] = dict()
e['C'] = dict()
e['D'] = dict()
e['E'] = dict()

# Row A: 2, 3, 4, 1, 7
e['A']['I'] = 2
e['A']['II'] = 3
e['A']['III'] = 4
e['A']['IV'] = 1
e['A']['V'] = 7

# Row B: 3, 4, 2, 5, 6
e['B']['I'] = 3
e['B']['II'] = 4
e['B']['III'] = 2
e['B']['IV'] = 5
e['B']['V'] = 6

# Row C: 2, 5, 3, 4, 1
e['C']['I'] = 2
e['C']['II'] = 5
e['C']['III'] = 3
e['C']['IV'] = 4
e['C']['V'] = 1

# Row D: 5, 2, 3, 2, 5
e['D']['I'] = 5
e['D']['II'] = 2
e['D']['III'] = 3
e['D']['IV'] = 2
e['D']['V'] = 5

# Row E: 3, 7, 6, 2, 4
e['E']['I'] = 3
e['E']['II'] = 7
e['E']['III'] = 6
e['E']['IV'] = 2
e['E']['V'] = 4

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for w in W:
    for s in S:
        x[w, s] = solver.BoolVar('x_' + w + '_' + s)

Z = solver.NumVar(0, INF, 'Z')

# Constraints
# 1. Each worker assigned to exactly one station
for w in W:
    solver.Add(sum(x[w, s] for s in S) == 1)

# 2. Each station operated by exactly one worker
for s in S:
    solver.Add(sum(x[w, s] for w in W) == 1)

# 3. Bottleneck definition: Z <= efficiency of each station
for s in S:
    solver.Add(Z <= sum(e[w][s] * x[w, s] for w in W))

# Objective: Maximize Z
solver.Maximize(Z)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")