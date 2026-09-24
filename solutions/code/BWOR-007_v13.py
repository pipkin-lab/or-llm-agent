from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
C = dict()
C[1] = -12
C[2] = -10
C[3] = -8
C[4] = -10
C[5] = -4
C[6] = 5
C[7] = -7
C[8] = -2
C[9] = 15
C[10] = 12
C[11] = -7
C[12] = 45

r_S = 0.015
r_D = 0.004
r_A = 0.01

# Decision variables
LA = solver.NumVar(0, INF, 'LA')
S = dict()
D = dict()
B = dict()
for t in range(1, 13):
    S[t] = solver.NumVar(0, INF, 'S_' + str(t))
    D[t] = solver.NumVar(0, INF, 'D_' + str(t))
    B[t] = solver.NumVar(0, INF, 'B_' + str(t))

# Constraints: Month 1
# B_1 = LA + S_1 + C_1 + 0.004 * D_1
solver.Add(B[1] == LA + S[1] + C[1] + r_D * D[1])

# Constraints: Months 2-12
for t in range(2, 13):
    # B_t = B_{t-1} + S_t - (1+r_S)*S_{t-1} + C_t + r_D*D_t - r_A*LA
    solver.Add(B[t] == B[t - 1] + S[t] - (1 + r_S) * S[t - 1] + C[t] + r_D * D[t] - r_A * LA)

# Objective: Maximize B_12
solver.Maximize(B[12])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")