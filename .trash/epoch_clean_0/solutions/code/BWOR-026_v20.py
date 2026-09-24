from ortools.linear_solver import pywraplp

# Problem parameters
n_jobs = 12
jobs = list(range(1, n_jobs + 1))

pA = dict()
pA[1] = 5
pA[2] = 8
pA[3] = 11
pA[4] = 2
pA[5] = 7
pA[6] = 6
pA[7] = 3
pA[8] = 9
pA[9] = 8
pA[10] = 3
pA[11] = 6
pA[12] = 10

pB = dict()
pB[1] = 5
pB[2] = 9
pB[3] = 4
pB[4] = 3
pB[5] = 7
pB[6] = 9
pB[7] = 5
pB[8] = 4
pB[9] = 9
pB[10] = 5
pB[11] = 3
pB[12] = 4

M_BIG = 100

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for j in jobs:
    for k in range(1, n_jobs + 1):
        x[j, k] = solver.IntVar(0, 1, 'x_%d_%d' % (j, k))

sA = dict()
for j in jobs:
    sA[j] = solver.NumVar(0, INF, 'sA_%d' % j)

sB = dict()
for j in jobs:
    sB[j] = solver.NumVar(0, INF, 'sB_%d' % j)

u = dict()
for i in jobs:
    for j in jobs:
        if i < j:
            u[i, j] = solver.IntVar(0, 1, 'u_%d_%d' % (i, j))

Cmax = solver.NumVar(0, INF, 'Cmax')

# Objective
solver.Minimize(Cmax)

# Assignment constraints
for j in jobs:
    solver.Add(sum(x[j, k] for k in range(1, n_jobs + 1)) == 1)

for k in range(1, n_jobs + 1):
    solver.Add(sum(x[j, k] for j in jobs) == 1)

# Precedence consistency (permutation schedule)
for i in jobs:
    for j in jobs:
        if i < j:
            solver.Add(u[i, j] + u[j, i] == 1)

            # Machine A sequencing
            solver.Add(sA[j] >= sA[i] + pA[i] - M_BIG * (1 - u[i, j]))
            solver.Add(sA[i] >= sA[j] + pA[j] - M_BIG * u[i, j])

            # Machine B sequencing
            solver.Add(sB[j] >= sB[i] + pB[i] - M_BIG * (1 - u[i, j]))
            solver.Add(sB[i] >= sB[j] + pB[j] - M_BIG * u[i, j])

# Job routing (internal precedence)
for j in range(1, 8):  # Jobs 1-7: A then B
    solver.Add(sB[j] >= sA[j] + pA[j])

for j in range(8, 13):  # Jobs 8-12: B then A
    solver.Add(sA[j] >= sB[j] + pB[j])

# Makespan definition
for j in jobs:
    solver.Add(Cmax >= sA[j] + pA[j])
    solver.Add(Cmax >= sB[j] + pB[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")