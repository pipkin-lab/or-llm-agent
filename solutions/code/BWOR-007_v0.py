from ortools.linear_solver import pywraplp

# Parameters
c = dict()
c[1] = -12
c[2] = -10
c[3] = -8
c[4] = -10
c[5] = -4
c[6] = 5
c[7] = -7
c[8] = -2
c[9] = 15
c[10] = 12
c[11] = -7
c[12] = 45

r_A = 0.01
r_S = 0.015
r_D = 0.004
N = 12

# Solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision Variables
A = solver.NumVar(0, INF, 'A')

B = dict()
D = dict()
C = dict()

for t in range(1, 13):
    B[t] = solver.NumVar(0, INF, 'B_' + str(t))
    D[t] = solver.NumVar(0, INF, 'D_' + str(t))

for t in range(1, 14):
    C[t] = solver.NumVar(0, INF, 'C_' + str(t))

# Constraint 1: C_1 = A
solver.Add(C[1] == A)

# Constraint 2 & 3: Cash Balance Recursion
for t in range(1, 12):
    # c'_t = c_t - r_A * A for t >= 2, c'_1 = c_1
    if t == 1:
        c_prime_t = c[1]
    else:
        c_prime_t = c[t] - r_A * A
    
    # C_{t+1} = C_t + c'_t - r_S * B_t + r_D * D_t
    # Rearranged for solver.Add:
    # C_{t+1} - C_t + r_S * B_t - r_D * D_t == c'_t
    # Note: c_prime_t contains -r_A*A, so we move it or keep as is.
    # Let's write: C[t+1] - C[t] + r_S*B[t] - r_D*D[t] + r_A*A (if t>1) == c[t]
    # Actually, let's stick to the definition:
    # C[t+1] = C[t] + (c[t] - (r_A*A if t>1 else 0)) - r_S*B[t] + r_D*D[t]
    # C[t+1] - C[t] + r_S*B[t] - r_D*D[t] - (r_A*A if t>1 else 0) == c[t]
    
    if t == 1:
        solver.Add(C[t+1] - C[t] + r_S * B[t] - r_D * D[t] == c[t])
    else:
        solver.Add(C[t+1] - C[t] + r_S * B[t] - r_D * D[t] - r_A * A == c[t])

# For t = 12
# C[13] = C[12] + c[12] - r_A*A - r_S*B[12] + r_D*D[12]
solver.Add(C[13] - C[12] + r_S * B[12] - r_D * D[12] - r_A * A == c[12])

# Constraint 4: Solvency Constraints
# C_t + B_t - D_t + c'_t >= 0
for t in range(1, 13):
    if t == 1:
        # C[1] + B[1] - D[1] + c[1] >= 0
        solver.Add(C[t] + B[t] - D[t] + c[t] >= 0)
    else:
        # C[t] + B[t] - D[t] + c[t] - r_A*A >= 0
        solver.Add(C[t] + B[t] - D[t] + c[t] - r_A * A >= 0)

# Objective: Maximize C[13]
solver.Maximize(C[13])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")