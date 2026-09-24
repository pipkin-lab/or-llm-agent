from ortools.linear_solver import pywraplp

# Data
n = 12
jobs = list(range(1, n + 1))

# Processing times
P_A = dict()
P_B = dict()

# Jobs 1-7: A -> B
P_A[1] = 5; P_B[1] = 5
P_A[2] = 8; P_B[2] = 9
P_A[3] = 11; P_B[3] = 4
P_A[4] = 2; P_B[4] = 3
P_A[5] = 7; P_B[5] = 7
P_A[6] = 6; P_B[6] = 9
P_A[7] = 3; P_B[7] = 5

# Jobs 8-12: B -> A
P_B[8] = 4; P_A[8] = 9
P_B[9] = 9; P_A[9] = 8
P_B[10] = 5; P_A[10] = 3
P_B[11] = 3; P_A[11] = 6
P_B[12] = 4; P_A[12] = 10

# Groups
group_AB = [1, 2, 3, 4, 5, 6, 7]
group_BA = [8, 9, 10, 11, 12]

# Solver (MILP)
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Variables
# Start times
S_A = dict()
S_B = dict()
for i in jobs:
    S_A[i] = solver.NumVar(0, INF, 'S_A_' + str(i))
    S_B[i] = solver.NumVar(0, INF, 'S_B_' + str(i))

# Makespan
Cmax = solver.NumVar(0, INF, 'Cmax')

# Big M for sequencing constraints
# Max possible makespan upper bound: sum of all processing times on each machine
sum_PA = sum(P_A[i] for i in jobs)
sum_PB = sum(P_B[i] for i in jobs)
M = sum_PA + sum_PB + 1

# Binary variables for sequencing on Machine A (for jobs that visit A)
# Jobs 1-7 and 8-12 all visit A
# yA[i,k] = 1 if job i is before job k on Machine A
# We only need yA for pairs of jobs that both visit A
# All 12 jobs visit A (1-7 first, 8-12 second)
# But the "sequence" interpretation: the global permutation defines order on first machine of each group.
# Let's re-read carefully. The problem states:
# "The order on Machine A for Jobs 1-7 follows the relative order in pi."
# "The order on Machine B for Jobs 8-12 follows the relative order in pi."
# And then: "the order on the second machine is determined by the earliest available time"
# This implies we do NOT fix the order on the second machine via binary variables.
# We only fix the order on the FIRST machine for each group.
# For group AB: First machine is A. So order on A for 1-7 is fixed by pi.
# For group BA: First machine is B. So order on B for 8-12 is fixed by pi.
# The second machine order is free, determined by constraints.

# So we need:
# 1. Binary variables for order of jobs 1-7 on Machine A.
# 2. Binary variables for order of jobs 8-12 on Machine B.
# 3. Start times S_A, S_B for all jobs.
# 4. Precedence constraints.
# 5. Machine non-overlap constraints for the SECOND machines (B for 1-7, A for 8-12) using big-M with binary variables?
#    No, the problem says the order on the second machine is determined by flow shop dynamics.
#    This means we need to ensure non-overlap on the second machines, but the order is not fixed.
#    So we need binary variables for non-overlap on the second machines too, OR we use the fact that
#    in a flow shop, the order on the second machine is the same as the order of completion on the first machine.
#    But that's not necessarily true if there are blocking issues, but in standard flow shop it is.
#    Actually, in a standard two-machine flow shop, the optimal schedule is a permutation schedule,
#    meaning the order on both machines is the same. But here we have mixed routing.
#    Let's stick to the most general formulation:
#    - Fix order on first machine for each group using binary variables.
#    - For second machine, use big-M constraints with binary variables to enforce non-overlap,
#      but the order is free.

# Let's define:
# For group AB (jobs 1-7):
#   yA[i,k] = 1 if i before k on A (i,k in 1-7)
#   yB[i,k] = 1 if i before k on B (i,k in 1-7)
# For group BA (jobs 8-12):
#   yB[j,l] = 1 if j before l on B (j,l in 8-12)
#   yA[j,l] = 1 if j before l on A (j,l in 8-12)

# But wait, the problem says "the sequence defines the order on the first machine".
# So for group AB, yA is fixed by the permutation. We don't need to make it a variable;
# we can just add constraints based on the permutation. But we are optimizing over the permutation.
# So we DO need yA as variables, but we need to enforce that they represent a permutation.
# This is getting complex. Let's use the standard formulation:
# For each machine, for each pair of jobs that visit that machine, we have a binary variable
# indicating the order, and we add the big-M constraints.

# Jobs visiting A: 1-7 and 8-12 (all 12 jobs)
# Jobs visiting B: 1-7 and 8-12 (all 12 jobs)

# So we need:
# yA[i,k] for all i,k in jobs, i != k
# yB[i,k] for all i,k in jobs, i != k

# But this is a lot of variables. 12*11 = 132 for each machine, 264 total.
# Let's do it.

yA = dict()
yB = dict()
for i in jobs:
    for k in jobs:
        if i != k:
            yA[i, k] = solver.BoolVar('yA_' + str(i) + '_' + str(k))
            yB[i, k] = solver.BoolVar('yB_' + str(i) + '_' + str(k))

# Constraints: yA[i,k] + yA[k,i] = 1
for i in jobs:
    for k in jobs:
        if i < k:
            solver.Add(yA[i, k] + yA[k, i] == 1)
            solver.Add(yB[i, k] + yB[k, i] == 1)

# Precedence constraints
for i in group_AB:
    solver.Add(S_B[i] >= S_A[i] + P_A[i])
for j in group_BA:
    solver.Add(S_A[j] >= S_B[j] + P_B[j])

# Machine non-overlap constraints
# On Machine A: for all i,k in jobs, i != k
for i in jobs:
    for k in jobs:
        if i < k:
            # S_A[k] >= S_A[i] + P_A[i] - M * (1 - yA[i,k])
            solver.Add(S_A[k] >= S_A[i] + P_A[i] - M * (1 - yA[i, k]))
            # S_A[i] >= S_A[k] + P_A[k] - M * yA[i,k]
            solver.Add(S_A[i] >= S_A[k] + P_A[k] - M * yA[i, k])

# On Machine B: for all i,k in jobs, i != k
for i in jobs:
    for k in jobs:
        if i < k:
            # S_B[k] >= S_B[i] + P_B[i] - M * (1 - yB[i,k])
            solver.Add(S_B[k] >= S_B[i] + P_B[i] - M * (1 - yB[i, k]))
            # S_B[i] >= S_B[k] + P_B[k] - M * yB[i,k]
            solver.Add(S_B[i] >= S_B[k] + P_B[k] - M * yB[i, k])

# Makespan constraints
for i in group_AB:
    solver.Add(Cmax >= S_B[i] + P_B[i])
for j in group_BA:
    solver.Add(Cmax >= S_A[j] + P_A[j])

# Objective
solver.Minimize(Cmax)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")