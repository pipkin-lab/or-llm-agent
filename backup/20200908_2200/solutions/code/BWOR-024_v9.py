from ortools.linear_solver import pywraplp

# Parameters
n = 6
a = [0, 30, 60, 60, 20, 80, 90]  # 1-indexed
b = [0, 70, 70, 50, 60, 30, 40]  # 1-indexed
M = 660

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision Variables
# z[i, j] for i < j: 1 if job i is before job j
z = dict()
for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
        z[i, j] = solver.BoolVar('z_' + str(i) + '_' + str(j))

# Continuous variables for start times and makespan
SA = dict()
SB = dict()
for j in range(1, n + 1):
    SA[j] = solver.NumVar(0, solver.infinity(), 'SA_' + str(j))
    SB[j] = solver.NumVar(0, solver.infinity(), 'SB_' + str(j))

Z = solver.NumVar(0, solver.infinity(), 'Z')

# Objective: Minimize makespan
solver.Minimize(Z)

# Constraints
for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
        # Machine A sequencing
        # If z[i,j] = 1 (i before j): SA[j] >= SA[i] + a[i]
        solver.Add(SA[j] >= SA[i] + a[i] - M * (1 - z[i, j]))
        # If z[i,j] = 0 (j before i): SA[i] >= SA[j] + a[j]
        solver.Add(SA[i] >= SA[j] + a[j] - M * z[i, j])

        # Machine B sequencing
        # If z[i,j] = 1 (i before j): SB[j] >= SB[i] + b[i]
        solver.Add(SB[j] >= SB[i] + b[i] - M * (1 - z[i, j]))
        # If z[i,j] = 0 (j before i): SB[i] >= SB[j] + b[j]
        solver.Add(SB[i] >= SB[j] + b[j] - M * z[i, j])

    # Flow constraints: Job j cannot start on B until it finishes on A
    solver.Add(SB[i] >= SA[i] + a[i])

# Makespan definition
for j in range(1, n + 1):
    solver.Add(Z >= SB[j] + b[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")