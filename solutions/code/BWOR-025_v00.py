from ortools.linear_solver import pywraplp

# Data parameters
n = 12
jobs = list(range(1, n + 1))

pA = dict()
pB = dict()
data = {
    1: (5, 5),
    2: (8, 9),
    3: (11, 4),
    4: (2, 3),
    5: (7, 7),
    6: (6, 9),
    7: (3, 5),
    8: (9, 4),
    9: (8, 9),
    10: (3, 5),
    11: (6, 3),
    12: (10, 4)
}
for i in jobs:
    pA[i] = data[i][0]
    pB[i] = data[i][1]

M_BIG = sum(pA.values()) + sum(pB.values())

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Binary variables x[i,j] for i < j (x[i,j]=1 if i before j)
x = dict()
for i in jobs:
    for j in jobs:
        if i < j:
            x[i, j] = solver.BoolVar('x_%d_%d' % (i, j))

# Continuous variables: start and completion times on both machines
SA = dict()
CA = dict()
SB = dict()
CB = dict()
for i in jobs:
    SA[i] = solver.NumVar(0, INF, 'SA_%d' % i)
    CA[i] = solver.NumVar(0, INF, 'CA_%d' % i)
    SB[i] = solver.NumVar(0, INF, 'SB_%d' % i)
    CB[i] = solver.NumVar(0, INF, 'CB_%d' % i)

Cmax = solver.NumVar(0, INF, 'Cmax')

# Constraints: completion = start + processing time
for i in jobs:
    solver.Add(CA[i] == SA[i] + pA[i])
    solver.Add(CB[i] == SB[i] + pB[i])

# Machine A sequencing: if i before j then SA[j] >= CA[i], else SA[i] >= CA[j]
for i in jobs:
    for j in jobs:
        if i == j:
            continue
        if i < j:
            # x[i,j]=1 means i before j => SA[j] >= CA[i]
            solver.Add(SA[j] >= CA[i] - M_BIG * (1 - x[i, j]))
            # x[i,j]=0 means j before i => SA[i] >= CA[j]
            solver.Add(SA[i] >= CA[j] - M_BIG * x[i, j])
        else:
            # j < i, variable is x[j,i]
            # x[j,i]=1 means j before i => SA[i] >= CA[j]
            solver.Add(SA[i] >= CA[j] - M_BIG * (1 - x[j, i]))
            # x[j,i]=0 means i before j => SA[j] >= CA[i]
            solver.Add(SA[j] >= CA[i] - M_BIG * x[j, i])

# Flow constraint: SB[i] >= CA[i]
for i in jobs:
    solver.Add(SB[i] >= CA[i])

# Machine B sequencing: if i before j then SB[j] >= CB[i], else SB[i] >= CB[j]
for i in jobs:
    for j in jobs:
        if i == j:
            continue
        if i < j:
            # x[i,j]=1 means i before j => SB[j] >= CB[i]
            solver.Add(SB[j] >= CB[i] - M_BIG * (1 - x[i, j]))
            # x[i,j]=0 means j before i => SB[i] >= CB[j]
            solver.Add(SB[i] >= CB[j] - M_BIG * x[i, j])
        else:
            # j < i, variable is x[j,i]
            # x[j,i]=1 means j before i => SB[i] >= CB[j]
            solver.Add(SB[i] >= CB[j] - M_BIG * (1 - x[j, i]))
            # x[j,i]=0 means i before j => SB[j] >= CB[i]
            solver.Add(SB[j] >= CB[i] - M_BIG * x[j, i])

# Makespan definition
for i in jobs:
    solver.Add(Cmax >= CB[i])

# Objective: minimize makespan
solver.Minimize(Cmax)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")