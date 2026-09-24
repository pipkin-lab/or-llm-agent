from ortools.linear_solver import pywraplp

# ------------------------------------------------------------------
# Two-machine flow shop scheduling (PFSP), 1-indexed positions 1..12
# Minimize makespan C_max. Solved as a MILP with SCIP.
# ------------------------------------------------------------------

# Jobs are 1-indexed: 1..12
pA = dict()
pB = dict()
# pA[i] = processing time of job i on Machine A
# pB[i] = processing time of job i on Machine B
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

jobs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Big-M: an upper bound on the makespan.
# Sum of all A times + sum of all B times is a safe upper bound.
sum_A = sum(pA[i] for i in jobs)
sum_B = sum(pB[i] for i in jobs)
BIG_M = sum_A + sum_B

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# ---- Decision variables ----
# pos[i, p] = 1 if job i is placed at position p
pos = dict()
for i in jobs:
    for p in positions:
        pos[i, p] = solver.BoolVar('pos_' + str(i) + '_' + str(p))

# x[i, p] = start time of job i on Machine A, if it is at position p
x = dict()
for i in jobs:
    for p in positions:
        x[i, p] = solver.NumVar(0, BIG_M, 'x_' + str(i) + '_' + str(p))

# y[i, p] = start time of job i on Machine B, if it is at position p
y = dict()
for i in jobs:
    for p in positions:
        y[i, p] = solver.NumVar(0, BIG_M, 'y_' + str(i) + '_' + str(p))

# C_max = makespan
Cmax = solver.NumVar(0, BIG_M, 'Cmax')

# ---- Assignment constraints ----
# Each job assigned to exactly one position
for i in jobs:
    solver.Add(sum(pos[i, p] for p in positions) == 1)

# Each position filled by exactly one job
for p in positions:
    solver.Add(sum(pos[i, p] for i in jobs) == 1)

# ---- Sequencing on Machine A (no overlap, positions ordered) ----
# For p >= 2: the job at position p starts no earlier than the job at
# position p-1 finishes on A. Using the big-M linearization with pos.
for i in jobs:
    for p in positions:
        if p >= 2:
            solver.Add(x[i, p] >= sum(
                x[j, p - 1] + pA[j] * pos[j, p - 1] for j in jobs
            ) - BIG_M * (1 - pos[i, p]))

# ---- Sequencing on Machine B (no overlap, positions ordered) ----
for i in jobs:
    for p in positions:
        if p >= 2:
            solver.Add(y[i, p] >= sum(
                y[j, p - 1] + pB[j] * pos[j, p - 1] for j in jobs
            ) - BIG_M * (1 - pos[i, p]))

# ---- Flow-shop precedence: B starts a job only after A finishes it ----
for i in jobs:
    for p in positions:
        solver.Add(y[i, p] >= x[i, p] + pA[i] * pos[i, p])

# ---- Makespan: C_max >= completion of every job on Machine B ----
for i in jobs:
    for p in positions:
        solver.Add(Cmax >= y[i, p] + pB[i] * pos[i, p])

# ---- Objective: minimize makespan ----
solver.Minimize(Cmax)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", Cmax.solution_value())
else:
    print("NO_FEASIBLE_SOLUTION")