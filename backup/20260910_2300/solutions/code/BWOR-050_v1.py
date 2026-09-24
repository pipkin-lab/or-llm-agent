from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
inf = solver.infinity()

# Index sets
athletes = ['Zhao', 'Qian', 'Zhang', 'Wang', 'Zhou']
strokes = ['Backstroke', 'Breaststroke', 'Butterfly', 'Freestyle']

# Time data t[i][j] where i is athlete index, j is stroke index
# Athletes: 0=Zhao, 1=Qian, 2=Zhang, 3=Wang, 4=Zhou
# Strokes: 0=Backstroke, 1=Breaststroke, 2=Butterfly, 3=Freestyle
times = [
    [37.7, 43.4, 33.3, 29.2],  # Zhao
    [32.9, 33.1, 28.5, 26.4],  # Qian
    [33.8, 42.2, 38.9, 29.6],  # Zhang
    [37.0, 34.7, 30.4, 28.5],  # Wang
    [35.4, 41.8, 33.6, 31.1],  # Zhou
]

# Decision variables: x[i][j] = 1 if athlete i is assigned to stroke j
x = dict()
for i in range(len(athletes)):
    for j in range(len(strokes)):
        x[i, j] = solver.BoolVar('x_{}{}'.format(i, j))

# Objective function: minimize total time
obj = 0
for i in range(len(athletes)):
    for j in range(len(strokes)):
        obj += times[i][j] * x[i, j]

solver.Minimize(obj)

# Constraint 1: Each stroke must be assigned to exactly one athlete
for j in range(len(strokes)):
    constraint = 0
    for i in range(len(athletes)):
        constraint += x[i, j]
    solver.Add(constraint == 1)

# Constraint 2: Each athlete can be assigned to at most one stroke
for i in range(len(athletes)):
    constraint = 0
    for j in range(len(strokes)):
        constraint += x[i, j]
    solver.Add(constraint <= 1)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")