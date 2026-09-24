from ortools.linear_solver import pywraplp

# Problem data
N = 12
# Jobs 1-7: A -> B, Jobs 8-12: B -> A
# p[j][0] = processing time on A, p[j][1] = processing time on B
# 1-indexed: j from 1 to 12
p = {
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

J = list(range(1, N + 1))
J_AB = list(range(1, 8))   # Jobs 1-7
J_BA = list(range(8, 13))  # Jobs 8-12

# Big-M: sum of all processing times
M = sum(p[j][0] + p[j][1] for j in J)

solver = pywraplp.Solver.CreateSolver('SCIP')

# Variables
# z[j, k] = 1 if job j precedes job k in the sequence, for j < k
z = dict()
for j in range(1, N + 1):
    for k in range(j + 1, N + 1):
        z[j, k] = solver.BoolVar('z_' + str(j) + '_' + str(k))

# S[j, 0] = start time on A, S[j, 1] = start time on B
S = dict()
for j in J:
    for m in range(2):
        S[j, m] = solver.NumVar(0, solver.infinity(), 'S_' + str(j) + '_' + str(m))

Cmax = solver.NumVar(0, solver.infinity(), 'Cmax')

# Constraints

# 1. Sequence definition: for j < k, z[j,k] + z[k,j] = 1
#    Since we only define z[j,k] for j<k, we need z[k,j] to be 1 - z[j,k]
#    So the constraint is implicit in the variable definition.
#    Actually, the mutual exclusivity is handled by the Big-M constraints using z[j,k] and (1-z[j,k]).
#    We don't need an explicit constraint here since z is binary and the Big-M constraints
#    will enforce the ordering. But to be safe, we can note that for j<k, z[k,j] = 1 - z[j,k].
#    In the Big-M constraints, we use z[j,k] for "j before k" and (1-z[j,k]) for "k before j".

# 2. Machine A availability (sequence constraint)
for j in J:
    for k in J:
        if j != k:
            if j < k:
                # z[j,k] = 1 if j before k
                # If j before k: S[j,0] + p[j,0] <= S[k,0]  =>  S[k,0] >= S[j,0] + p[j,0]
                # If k before j: S[k,0] + p[k,0] <= S[j,0]  =>  S[j,0] >= S[k,0] + p[k,0]
                z_jk = z[j, k]
                # Constraint 1: S[k,0] >= S[j,0] + p[j][0] - M*(1 - z[j,k])
                solver.Add(S[k, 0] >= S[j, 0] + p[j][0] - M * (1 - z_jk))
                # Constraint 2: S[j,0] >= S[k,0] + p[k][0] - M*(1 - z[k,j]) = M*z[j,k]
                # Since z[k,j] = 1 - z[j,k], so M*(1 - z[k,j]) = M*z[j,k]
                solver.Add(S[j, 0] >= S[k, 0] + p[k][0] - M * z_jk)
            else:
                # j > k, so we already handled this pair when k < j
                pass

# 3. Machine B availability (sequence constraint)
for j in J:
    for k in J:
        if j != k:
            if j < k:
                z_jk = z[j, k]
                solver.Add(S[k, 1] >= S[j, 1] + p[j][1] - M * (1 - z_jk))
                solver.Add(S[j, 1] >= S[k, 1] + p[k][1] - M * z_jk)
            else:
                pass

# 4. Routing constraints
# For Jobs 1-7 (A -> B): S[j,1] >= S[j,0] + p[j][0]
for j in J_AB:
    solver.Add(S[j, 1] >= S[j, 0] + p[j][0])

# For Jobs 8-12 (B -> A): S[j,0] >= S[j,1] + p[j][1]
for j in J_BA:
    solver.Add(S[j, 0] >= S[j, 1] + p[j][1])

# 5. Makespan definition
for j in J:
    solver.Add(Cmax >= S[j, 0] + p[j][0])
    solver.Add(Cmax >= S[j, 1] + p[j][1])

# Objective: Minimize Cmax
solver.Minimize(Cmax)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", Cmax.Value())
else:
    print("NO_FEASIBLE_SOLUTION")