from ortools.linear_solver import pywraplp

# Parameters
n_jobs = 12
n_pos = 12

a = [5, 8, 11, 2, 7, 6, 3, 9, 8, 3, 6, 10]
b = [5, 9, 4, 3, 7, 9, 5, 4, 9, 5, 3, 4]

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Variables
x = dict()
for j in range(n_jobs):
    for p in range(n_pos):
        x[j, p] = solver.BoolVar('x_' + str(j) + '_' + str(p))

S_A = dict()
C_A = dict()
S_B = dict()
C_B = dict()

for p in range(n_pos):
    S_A[p] = solver.NumVar(0, solver.infinity(), 'S_A_' + str(p))
    C_A[p] = solver.NumVar(0, solver.infinity(), 'C_A_' + str(p))
    S_B[p] = solver.NumVar(0, solver.infinity(), 'S_B_' + str(p))
    C_B[p] = solver.NumVar(0, solver.infinity(), 'C_B_' + str(p))

Z = solver.NumVar(0, solver.infinity(), 'Z')

# Assignment constraints
for j in range(n_jobs):
    solver.Add(sum(x[j, p] for p in range(n_pos)) == 1)

for p in range(n_pos):
    solver.Add(sum(x[j, p] for j in range(n_jobs)) == 1)

# Machine A constraints
solver.Add(S_A[0] == 0)

for p in range(n_pos):
    solver.Add(C_A[p] == S_A[p] + sum(a[j] * x[j, p] for j in range(n_jobs)))

for p in range(1, n_pos):
    solver.Add(S_A[p] == C_A[p - 1])

# Machine B constraints
for p in range(n_pos):
    solver.Add(S_B[p] >= C_A[p])

for p in range(1, n_pos):
    solver.Add(S_B[p] >= C_B[p - 1])

for p in range(n_pos):
    solver.Add(C_B[p] == S_B[p] + sum(b[j] * x[j, p] for j in range(n_jobs)))

# Makespan
solver.Add(Z >= C_B[n_pos - 1])

# Objective
solver.Minimize(Z)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")