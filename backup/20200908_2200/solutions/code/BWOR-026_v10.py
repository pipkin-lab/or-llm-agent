from ortools.linear_solver import pywraplp

# Problem data
n_jobs = 12
n_positions = 12

# Processing times on Machine A and B (1-indexed for clarity, 0-indexed in code)
a = [5, 8, 11, 2, 7, 6, 3, 9, 8, 3, 6, 10]
b = [5, 9, 4, 3, 7, 9, 5, 4, 9, 5, 3, 4]

# Sets
I_A = list(range(0, 7))   # Jobs 1-7 (0-6)
I_B = list(range(7, 12))  # Jobs 8-12 (7-11)

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    print("Could not create solver")
    exit(1)

inf = solver.infinity()

# Decision Variables
# y[i][j] = 1 if job i is in position j (0-indexed)
y = dict()
for i in range(n_jobs):
    for j in range(n_positions):
        y[i, j] = solver.BoolVar('y_' + str(i) + '_' + str(j))

# S_A[j] = start time of job in position j on Machine A
# S_B[j] = start time of job in position j on Machine B
S_A = dict()
S_B = dict()
for j in range(n_positions):
    S_A[j] = solver.NumVar(0, inf, 'S_A_' + str(j))
    S_B[j] = solver.NumVar(0, inf, 'S_B_' + str(j))

# C_max = makespan
C_max = solver.NumVar(0, inf, 'C_max')

# Constraints

# 1. Job Assignment Constraints
# Each job assigned to exactly one position
for i in range(n_jobs):
    solver.Add(sum(y[i, j] for j in range(n_positions)) == 1)

# Each position has exactly one job
for j in range(n_positions):
    solver.Add(sum(y[i, j] for i in range(n_jobs)) == 1)

# 2. Machine Sequencing Constraints
# For Machine A: S_A[j] >= S_A[j-1] + sum_k a_k * y[k][j-1]
for j in range(1, n_positions):
    # sum_k a_k * y[k][j-1] is the processing time on A for the job in position j-1
    proc_time_A_prev = sum(a[k] * y[k, j-1] for k in range(n_jobs))
    solver.Add(S_A[j] >= S_A[j-1] + proc_time_A_prev)

# For Machine B: S_B[j] >= S_B[j-1] + sum_k b_k * y[k][j-1]
for j in range(1, n_positions):
    # sum_k b_k * y[k][j-1] is the processing time on B for the job in position j-1
    proc_time_B_prev = sum(b[k] * y[k, j-1] for k in range(n_jobs))
    solver.Add(S_B[j] >= S_B[j-1] + proc_time_B_prev)

# 3. Routing Constraints
# For all positions j:
for j in range(n_positions):
    # If job in position j is Type A (in I_A), it must finish A before starting B.
    # Sum_{i in I_A} a_i * y[i][j] is the A-processing time if job is Type A, else 0.
    # Constraint: S_B[j] >= S_A[j] + (A-processing time if Type A)
    a_proc_if_type_A = sum(a[i] * y[i, j] for i in I_A)
    solver.Add(S_B[j] >= S_A[j] + a_proc_if_type_A)
    
    # If job in position j is Type B (in I_B), it must finish B before starting A.
    # Sum_{i in I_B} b_i * y[i][j] is the B-processing time if job is Type B, else 0.
    # Constraint: S_A[j] >= S_B[j] + (B-processing time if Type B)
    b_proc_if_type_B = sum(b[i] * y[i, j] for i in I_B)
    solver.Add(S_A[j] >= S_B[j] + b_proc_if_type_B)

# 4. Makespan Definition
# C_max >= Finish time on A for job in position j
# C_max >= Finish time on B for job in position j
for j in range(n_positions):
    finish_A_j = S_A[j] + sum(a[k] * y[k, j] for k in range(n_jobs))
    solver.Add(C_max >= finish_A_j)
    
    finish_B_j = S_B[j] + sum(b[k] * y[k, j] for k in range(n_jobs))
    solver.Add(C_max >= finish_B_j)

# Objective: Minimize C_max
solver.Minimize(C_max)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")