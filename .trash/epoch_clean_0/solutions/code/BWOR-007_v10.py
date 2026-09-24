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

r_annual = 0.01
repay_factor = 1.015
maturity_factor = 1.004

# Decision Variables
L_annual = solver.NumVar(0, INF, 'L_annual')

S = dict()
D = dict()
B = dict()

for t in range(1, 13):
    S[t] = solver.NumVar(0, INF, 'S_' + str(t))
    D[t] = solver.NumVar(0, INF, 'D_' + str(t))
    B[t] = solver.NumVar(0, INF, 'B_' + str(t))

# Cash Balance Constraints
# Month 1: B_1 = L_annual + S_1 + 0.004*D_1 + C_1
# L_annual + S_1 + 0.004*D_1 - B_1 = -C_1
solver.Add(L_annual + S[1] + 0.004 * D[1] - B[1] == -C[1])

# Months 2 to 12: B_t = B_{t-1} + S_t - 1.015*S_{t-1} + 0.004*D_t + C_t - 0.01*L_annual
# B_{t-1} + S_t - 1.015*S_{t-1} + 0.004*D_t - 0.01*L_annual - B_t = -C_t
for t in range(2, 13):
    solver.Add(B[t - 1] + S[t] - repay_factor * S[t - 1] + (maturity_factor - 1) * D[t] - r_annual * L_annual - B[t] == -C[t])

# Objective: Maximize B_12
solver.Maximize(B[12])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")