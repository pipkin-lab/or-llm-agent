from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets
S = ['I', 'II']
C = [1, 2, 3]

# Parameters
Cap = dict()
Cap['I'] = 400
Cap['II'] = 450

D_min = dict()
D_min[1] = 290
D_min[2] = 250
D_min[3] = 270

D_max = dict()
D_max[1] = 320
D_max[2] = 250
D_max[3] = 350

Cost = dict()
Cost[('I', 1)] = 15
Cost[('I', 2)] = 18
Cost[('I', 3)] = 22
Cost[('II', 1)] = 21
Cost[('II', 2)] = 25
Cost[('II', 3)] = 16

# Decision variables
x = dict()
for s in S:
    for c in C:
        x[s, c] = solver.NumVar(0, INF, 'x_' + s + '_' + str(c))

# Objective
obj = 0
for s in S:
    for c in C:
        obj += Cost[s, c] * x[s, c]
solver.Minimize(obj)

# Supply capacity constraints (must use up all available electricity)
for s in S:
    solver.Add(sum(x[s, c] for c in C) == Cap[s])

# Demand constraints
# City 1: 290 <= sum <= 320
solver.Add(sum(x[s, 1] for s in S) >= D_min[1])
solver.Add(sum(x[s, 1] for s in S) <= D_max[1])

# City 2: fixed at 250
solver.Add(sum(x[s, 2] for s in S) == D_min[2])

# City 3: 270 <= sum <= 350
solver.Add(sum(x[s, 3] for s in S) >= D_min[3])
solver.Add(sum(x[s, 3] for s in S) <= D_max[3])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")