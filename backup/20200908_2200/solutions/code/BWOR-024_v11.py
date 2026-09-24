from ortools.linear_solver import pywraplp

# Parameters
n = 6
a = [30, 60, 60, 20, 80, 90]
b = [70, 70, 50, 60, 30, 40]

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    print("Could not create solver")
    exit(1)

inf = solver.infinity()

# Variables
# x[j][k] = 1 if job j is at position k
x = dict()
for j in range(n):
    for k in range(n):
        x[j, k] = solver.BoolVar('x_' + str(j) + '_' + str(k))

# T_A[k]: start time of job in position k on machine A
T_A = dict()
for k in range(n):
    T_A[k] = solver.NumVar(0, inf, 'T_A_' + str(k))

# T_B[k]: start time of job in position k on machine B
T_B = dict()
for k in range(n):
    T_B[k] = solver.NumVar(0, inf, 'T_B_' + str(k))

# C_max
C_max = solver.NumVar(0, inf, 'C_max')

# Constraints

# 1. Assignment: each job to exactly one position
for j in range(n):
    solver.Add(sum(x[j, k] for k in range(n)) == 1)

# 2. Assignment: each position has exactly one job
for k in range(n):
    solver.Add(sum(x[j, k] for j in range(n)) == 1)

# 3. T_A[0] = 0
solver.Add(T_A[0] == 0)

# 4. T_A[k] - T_A[k-1] - sum_j a[j] * x[j][k-1] = 0 for k in 1..n-1
for k in range(1, n):
    solver.Add(T_A[k] - T_A[k-1] - sum(a[j] * x[j, k-1] for j in range(n)) == 0)

# 5. T_B[k] - T_A[k] - sum_j a[j] * x[j][k] >= 0 for all k
for k in range(n):
    solver.Add(T_B[k] - T_A[k] - sum(a[j] * x[j, k] for j in range(n)) >= 0)

# 6. T_B[k] - T_B[k-1] - sum_j b[j] * x[j][k-1] >= 0 for k in 1..n-1
for k in range(1, n):
    solver.Add(T_B[k] - T_B[k-1] - sum(b[j] * x[j, k-1] for j in range(n)) >= 0)

# 7. C_max - T_B[n-1] - sum_j b[j] * x[j][n-1] = 0
solver.Add(C_max - T_B[n-1] - sum(b[j] * x[j, n-1] for j in range(n)) == 0)

# Objective
solver.Minimize(C_max)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")