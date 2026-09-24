from ortools.linear_solver import pywraplp

# Parameters
T = range(1, 13)
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
B0 = 0

# Solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision Variables
L_A = solver.NumVar(0, INF, 'L_A')
S = dict()
D = dict()
B = dict()

for t in T:
    S[t] = solver.NumVar(0, INF, 'S_' + str(t))
    D[t] = solver.NumVar(0, INF, 'D_' + str(t))
    B[t] = solver.NumVar(0, INF, 'B_' + str(t))

# Constraints: Cash Balance Equations
# For t = 1
solver.Add(B[1] == B0 + S[1] + r_D * D[1] + c[1])

# For t = 2 to 11
for t in range(2, 12):
    solver.Add(B[t] == B[t - 1] + S[t] + r_D * D[t] - S[t - 1] * (1 + r_S) + c[t] - r_A * L_A)

# For t = 12
solver.Add(B[12] == B[11] + S[12] + r_D * D[12] - S[11] * (1 + r_S) + c[12] - r_A * L_A - L_A)

# Objective: Maximize B[12]
solver.Maximize(B[12])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")