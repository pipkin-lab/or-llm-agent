from ortools.linear_solver import pywraplp

# Parameters
n = 12
a = dict()
b = dict()
a[1] = 5;  b[1] = 5
a[2] = 8;  b[2] = 9
a[3] = 11; b[3] = 4
a[4] = 2;  b[4] = 3
a[5] = 7;  b[5] = 7
a[6] = 6;  b[6] = 9
a[7] = 3;  b[7] = 5
a[8] = 9;  b[8] = 4
a[9] = 8;  b[9] = 9
a[10] = 3; b[10] = 5
a[11] = 6; b[11] = 3
a[12] = 10; b[12] = 4

jobs = list(range(1, n + 1))
positions = list(range(1, n + 1))

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for j in jobs:
    for p in positions:
        x[j, p] = solver.BoolVar('x_' + str(j) + '_' + str(p))

SA = dict()
CA = dict()
SB = dict()
CB = dict()
for p in positions:
    SA[p] = solver.NumVar(0, INF, 'SA_' + str(p))
    CA[p] = solver.NumVar(0, INF, 'CA_' + str(p))
    SB[p] = solver.NumVar(0, INF, 'SB_' + str(p))
    CB[p] = solver.NumVar(0, INF, 'CB_' + str(p))

T = solver.NumVar(0, INF, 'T')

# Objective: minimize T
solver.Minimize(T)

# Constraint 1: Each job assigned to exactly one position
for j in jobs:
    solver.Add(sum(x[j, p] for p in positions) == 1)

# Constraint 2: Each position assigned exactly one job
for p in positions:
    solver.Add(sum(x[j, p] for j in jobs) == 1)

# Constraint 3: Machine A processing
solver.Add(SA[1] == 0)
for p in positions:
    solver.Add(CA[p] == SA[p] + sum(a[j] * x[j, p] for j in jobs))
for p in range(1, n):
    solver.Add(SA[p + 1] >= CA[p])

# Constraint 4: Machine B processing
for p in positions:
    solver.Add(SB[p] >= CA[p])
for p in range(1, n):
    solver.Add(SB[p + 1] >= CB[p])
for p in positions:
    solver.Add(CB[p] == SB[p] + sum(b[j] * x[j, p] for j in jobs))

# Constraint 5: Makespan
solver.Add(T == CB[n])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")