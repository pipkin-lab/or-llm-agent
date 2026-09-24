from ortools.linear_solver import pywraplp

# Parameters
J = list(range(1, 13))
J_AB = list(range(1, 8))   # Jobs 1-7: A -> B
J_BA = list(range(8, 13))  # Jobs 8-12: B -> A

# Processing times
tA = dict()
tB = dict()

tA[1] = 5;  tB[1] = 5
tA[2] = 8;  tB[2] = 9
tA[3] = 11; tB[3] = 4
tA[4] = 2;  tB[4] = 3
tA[5] = 7;  tB[5] = 7
tA[6] = 6;  tB[6] = 9
tA[7] = 3;  tB[7] = 5
tA[8] = 9;  tB[8] = 4
tA[9] = 8;  tB[9] = 9
tA[10] = 3; tB[10] = 5
tA[11] = 6; tB[11] = 3
tA[12] = 10; tB[12] = 4

M = 145

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision Variables
S_A = dict()
S_B = dict()
for j in J:
    S_A[j] = solver.NumVar(0, INF, 'S_A_' + str(j))
    S_B[j] = solver.NumVar(0, INF, 'S_B_' + str(j))

y = dict()
for j in J:
    for k in J:
        if j < k:
            y[j, k] = solver.BoolVar('y_' + str(j) + '_' + str(k))

C_max = solver.NumVar(0, INF, 'C_max')

# Objective
solver.Minimize(C_max)

# Sequencing Constraints on Machine A
for j in J:
    for k in J:
        if j < k:
            # S_A[k] >= S_A[j] + tA[j] - M*(1 - y[j,k])
            solver.Add(S_A[k] >= S_A[j] + tA[j] - M * (1 - y[j, k]))
            # S_A[j] >= S_A[k] + tA[k] - M*y[j,k]
            solver.Add(S_A[j] >= S_A[k] + tA[k] - M * y[j, k])

# Sequencing Constraints on Machine B
for j in J:
    for k in J:
        if j < k:
            # S_B[k] >= S_B[j] + tB[j] - M*(1 - y[j,k])
            solver.Add(S_B[k] >= S_B[j] + tB[j] - M * (1 - y[j, k]))
            # S_B[j] >= S_B[k] + tB[k] - M*y[j,k]
            solver.Add(S_B[j] >= S_B[k] + tB[k] - M * y[j, k])

# Job Flow Constraints
for j in J_AB:
    # S_B[j] >= S_A[j] + tA[j]
    solver.Add(S_B[j] >= S_A[j] + tA[j])

for j in J_BA:
    # S_A[j] >= S_B[j] + tB[j]
    solver.Add(S_A[j] >= S_B[j] + tB[j])

# Makespan Constraints
for j in J_AB:
    # C_max >= S_B[j] + tB[j]
    solver.Add(C_max >= S_B[j] + tB[j])

for j in J_BA:
    # C_max >= S_A[j] + tA[j]
    solver.Add(C_max >= S_A[j] + tA[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")