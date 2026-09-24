from ortools.linear_solver import pywraplp

# Parameters
J = [1, 2, 3, 4, 5, 6]
P = [1, 2, 3, 4, 5, 6]

a = dict()
a[1] = 30
a[2] = 60
a[3] = 60
a[4] = 20
a[5] = 80
a[6] = 90

b = dict()
b[1] = 70
b[2] = 70
b[3] = 50
b[4] = 60
b[5] = 30
b[6] = 40

T_max = 660

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for j in J:
    for p in P:
        x[j, p] = solver.BoolVar('x_' + str(j) + '_' + str(p))

sA = dict()
for j in J:
    sA[j] = solver.NumVar(0, INF, 'sA_' + str(j))

sB = dict()
for j in J:
    sB[j] = solver.NumVar(0, INF, 'sB_' + str(j))

Cmax = solver.NumVar(0, INF, 'Cmax')

# y variables: y[j,k] = 1 if job j is processed before job k
y = dict()
for j in J:
    for k in J:
        if j != k:
            y[j, k] = solver.BoolVar('y_' + str(j) + '_' + str(k))

# Assignment constraints: each job has exactly one position
for j in J:
    solver.Add(sum(x[j, p] for p in P) == 1)

# Position constraints: each position has exactly one job
for p in P:
    solver.Add(sum(x[j, p] for j in J) == 1)

# Consistency of sequence: y[j,k] + y[k,j] = 1 for all j != k
for j in J:
    for k in J:
        if j != k and j < k:
            solver.Add(y[j, k] + y[k, j] == 1)

# Precedence on Machine A
for j in J:
    for k in J:
        if j != k:
            # s_k,A >= s_j,A + a_j - T_max * (1 - y[j,k])
            solver.Add(sA[k] >= sA[j] + a[j] - T_max * (1 - y[j, k]))
            # s_j,A >= s_k,A + a_k - T_max * y[j,k]
            solver.Add(sA[j] >= sA[k] + a[k] - T_max * y[j, k])

# Precedence on Machine B
for j in J:
    for k in J:
        if j != k:
            # s_k,B >= s_j,B + b_j - T_max * (1 - y[j,k])
            solver.Add(sB[k] >= sB[j] + b[j] - T_max * (1 - y[j, k]))
            # s_j,B >= s_k,B + b_k - T_max * y[j,k]
            solver.Add(sB[j] >= sB[k] + b[k] - T_max * y[j, k])

# Flow constraint: job j cannot start on B until it finishes on A
for j in J:
    solver.Add(sB[j] >= sA[j] + a[j])

# Objective: Cmax >= s_j,B + b_j for all j
for j in J:
    solver.Add(Cmax >= sB[j] + b[j])

# Minimize makespan
solver.Minimize(Cmax)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")