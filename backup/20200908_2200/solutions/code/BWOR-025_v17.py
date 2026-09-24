from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

n_jobs = 12
n_pos = 12

# Data
t_A = [0, 5, 8, 11, 2, 7, 6, 3, 9, 8, 3, 6, 10]  # 1-indexed
t_B = [0, 5, 9, 4, 3, 7, 9, 5, 4, 9, 5, 3, 4]   # 1-indexed

# Variables
x = dict()
for i in range(1, n_jobs + 1):
    for p in range(1, n_pos + 1):
        x[i, p] = solver.BoolVar('x_' + str(i) + '_' + str(p))

C_A = dict()
for p in range(1, n_pos + 1):
    C_A[p] = solver.NumVar(0, solver.infinity(), 'C_A_' + str(p))

C_B = dict()
for p in range(1, n_pos + 1):
    C_B[p] = solver.NumVar(0, solver.infinity(), 'C_B_' + str(p))

Z = solver.NumVar(0, solver.infinity(), 'Z')

# Assignment constraints: each job to exactly one position
for i in range(1, n_jobs + 1):
    solver.Add(sum(x[i, p] for p in range(1, n_pos + 1)) == 1)

# Each position has exactly one job
for p in range(1, n_pos + 1):
    solver.Add(sum(x[i, p] for i in range(1, n_jobs + 1)) == 1)

# Machine A completion times
for p in range(1, n_pos + 1):
    expr = sum(t_A[i] * x[i, k] for k in range(1, p + 1) for i in range(1, n_jobs + 1))
    solver.Add(C_A[p] == expr)

# Machine B completion times (linearized max)
for p in range(1, n_pos + 1):
    proc_B = sum(t_B[i] * x[i, p] for i in range(1, n_jobs + 1))
    if p == 1:
        solver.Add(C_B[p] >= 0 + proc_B)
    else:
        solver.Add(C_B[p] >= C_B[p - 1] + proc_B)
    solver.Add(C_B[p] >= C_A[p] + proc_B)

# Makespan
solver.Add(Z == C_B[n_pos])

# Objective
solver.Minimize(Z)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")