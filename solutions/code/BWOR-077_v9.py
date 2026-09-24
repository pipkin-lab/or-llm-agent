from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

workers = ['A', 'B', 'C', 'D', 'E']
stations = ['I', 'II', 'III', 'IV', 'V']

e = dict()
e[('A', 'I')] = 2; e[('A', 'II')] = 3; e[('A', 'III')] = 4; e[('A', 'IV')] = 1; e[('A', 'V')] = 7
e[('B', 'I')] = 3; e[('B', 'II')] = 4; e[('B', 'III')] = 2; e[('B', 'IV')] = 5; e[('B', 'V')] = 6
e[('C', 'I')] = 2; e[('C', 'II')] = 5; e[('C', 'III')] = 3; e[('C', 'IV')] = 4; e[('C', 'V')] = 1
e[('D', 'I')] = 5; e[('D', 'II')] = 2; e[('D', 'III')] = 3; e[('D', 'IV')] = 2; e[('D', 'V')] = 5
e[('E', 'I')] = 3; e[('E', 'II')] = 7; e[('E', 'III')] = 6; e[('E', 'IV')] = 2; e[('E', 'V')] = 4

x = dict()
for w in workers:
    for s in stations:
        x[w, s] = solver.BoolVar('x_' + w + '_' + s)

Z = solver.NumVar(0, solver.infinity(), 'Z')

# A. Each station has exactly one worker
for s in stations:
    solver.Add(sum(x[w, s] for w in workers) == 1)

# B. Each worker is assigned to exactly one station
for w in workers:
    solver.Add(sum(x[w, s] for s in stations) == 1)

# C. Bottleneck definition constraints
for s in stations:
    solver.Add(Z <= sum(e[w, s] * x[w, s] for w in workers))

solver.Maximize(Z)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")