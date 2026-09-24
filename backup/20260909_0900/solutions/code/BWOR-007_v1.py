from ortools.linear_solver import pywraplp

# Parameters
C = [-12, -10, -8, -10, -4, 5, -7, -2, 15, 12, -7, 45]
r_annual = 0.01
r_short = 0.015
r_dep = 0.004
T = range(1, 13)

# Solver
solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Variables
A = solver.NumVar(0, inf, 'A')

L = dict()
for t in T:
    L[t] = solver.NumVar(0, inf, 'L_' + str(t))

D = dict()
for t in T:
    D[t] = solver.NumVar(0, inf, 'D_' + str(t))

B = dict()
for t in T:
    B[t] = solver.NumVar(0, inf, 'B_' + str(t))

# Constraints
# Month 1 Balance: B_1 = A + L_1 + C[0] + 0.004 * D_1
solver.Add(B[1] == A + L[1] + C[0] + r_dep * D[1])

# Month t Balance for t = 2 to 12
# B_t = B_{t-1} + L_t + C[t-1] - 1.015 * L_{t-1} - 0.01 * A + 0.004 * D_t
for t in range(2, 13):
    solver.Add(B[t] == B[t-1] + L[t] + C[t-1] - (1 + r_short) * L[t-1] - r_annual * A + r_dep * D[t])

# Objective: Maximize Z = B_12 - 1.015 * L_12
objective = solver.Maximize(B[12] - (1 + r_short) * L[12])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")