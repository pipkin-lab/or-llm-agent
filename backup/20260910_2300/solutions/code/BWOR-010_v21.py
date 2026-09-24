from ortools.linear_solver import pywraplp

# Index sets
I = [1, 2, 3]
J = [1, 2, 3]

# Parameters
S = dict()
S[1] = 20
S[2] = 30
S[3] = 20

D = dict()
D[1] = 15
D[2] = 25
D[3] = 20

C = dict()
C[1, 1] = 3
C[1, 2] = 10
C[1, 3] = 2
C[2, 1] = 4
C[2, 2] = 11
C[2, 3] = 8
C[3, 1] = 8
C[3, 2] = 11
C[3, 3] = 4

P = dict()
P[1] = 12
P[2] = 16
P[3] = 11

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_%d_%d' % (i, j))

# Objective: maximize sum of (P_j - C_ij) * x_ij
obj = 0
for i in I:
    for j in J:
        obj += (P[j] - C[i, j]) * x[i, j]

solver.Maximize(obj)

# Supply constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= S[i])

# Demand constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) <= D[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")