from ortools.linear_solver import pywraplp

# Parameters
jobs = [1, 2, 3, 4, 5, 6]
A = dict()
A[1] = 30
A[2] = 60
A[3] = 60
A[4] = 20
A[5] = 80
A[6] = 90

B = dict()
B[1] = 70
B[2] = 70
B[3] = 50
B[4] = 60
B[5] = 30
B[6] = 40

M = 660

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision Variables
CA = dict()
CB = dict()
for j in jobs:
    CA[j] = solver.NumVar(0, INF, 'CA_' + str(j))
    CB[j] = solver.NumVar(0, INF, 'CB_' + str(j))

# Binary sequencing variables x[i][j] for i != j
x = dict()
for i in jobs:
    for j in jobs:
        if i != j:
            x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

Cmax = solver.NumVar(0, INF, 'Cmax')

# Objective: minimize Cmax
solver.Minimize(Cmax)

# Constraint 1: Cmax >= CB[j] for all j
for j in jobs:
    solver.Add(Cmax >= CB[j])

# Constraint 2: Machine A non-overlap
for i in jobs:
    for j in jobs:
        if i != j:
            solver.Add(CA[j] >= CA[i] + A[j] - M * (1 - x[i, j]))

# Constraint 3: Machine B non-overlap
for i in jobs:
    for j in jobs:
        if i != j:
            solver.Add(CB[j] >= CB[i] + B[j] - M * (1 - x[i, j]))

# Constraint 4: Flow shop transition A to B
for j in jobs:
    solver.Add(CB[j] >= CA[j] + B[j])

# Constraint 5: x[i][j] + x[j][i] = 1 for i < j
for i in jobs:
    for j in jobs:
        if i < j:
            solver.Add(x[i, j] + x[j, i] == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")