from ortools.linear_solver import pywraplp

# Parameters
jobs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
n = len(jobs)

a = dict()
b = dict()
a[1] = 5
a[2] = 8
a[3] = 11
a[4] = 2
a[5] = 7
a[6] = 6
a[7] = 3
a[8] = 9
a[9] = 8
a[10] = 3
a[11] = 6
a[12] = 10

b[1] = 5
b[2] = 9
b[3] = 4
b[4] = 3
b[5] = 7
b[6] = 9
b[7] = 5
b[8] = 4
b[9] = 9
b[10] = 5
b[11] = 3
b[12] = 4

# Solve using MILP
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for j in jobs:
    for p in positions:
        x[j, p] = solver.BoolVar('x_{}_{}'.format(j, p))

CA = dict()
CB = dict()
M = dict()
for p in positions:
    CA[p] = solver.NumVar(0, INF, 'CA_{}'.format(p))
    CB[p] = solver.NumVar(0, INF, 'CB_{}'.format(p))
    M[p] = solver.NumVar(0, INF, 'M_{}'.format(p))

# Constraint 1: Each job assigned to exactly one position
for j in jobs:
    solver.Add(sum(x[j, p] for p in positions) == 1)

# Constraint 2: Each position assigned exactly one job
for p in positions:
    solver.Add(sum(x[j, p] for j in jobs) == 1)

# Constraint 3: Machine A completion times
CA[1] = None
for p in positions:
    if p == 1:
        solver.Add(CA[p] == sum(a[j] * x[j, 1] for j in jobs))
    else:
        solver.Add(CA[p] == CA[p - 1] + sum(a[j] * x[j, p] for j in jobs))

# Constraint 4: Machine B completion times (linearized with M_p)
for p in positions:
    if p == 1:
        solver.Add(M[p] >= CA[p])
        solver.Add(CB[p] == M[p] + sum(b[j] * x[j, 1] for j in jobs))
    else:
        solver.Add(M[p] >= CA[p])
        solver.Add(M[p] >= CB[p - 1])
        solver.Add(CB[p] == M[p] + sum(b[j] * x[j, p] for j in jobs))

# Objective: minimize makespan C = CB(12)
solver.Minimize(CB[12])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")