from ortools.linear_solver import pywraplp

# Index sets
T = list(range(1, 7))   # Months 1..6
J = list(range(1, 8))   # Products 1..7
M = list(range(1, 6))   # Machine types 1..5

# Parameters
c = {1: 100, 2: 60, 3: 80, 4: 40, 5: 110, 6: 90, 7: 30}
h = 5
H_max = 100

# Demand D[t, j] for t in 1..6, j in 1..7 (Table C-4 from problem)
D = dict()
D[1] = dict()
D[1][1] = 30; D[1][2] = 40; D[1][3] = 25; D[1][4] = 35; D[1][5] = 20; D[1][6] = 30; D[1][7] = 15
D[2] = dict()
D[2][1] = 25; D[2][2] = 35; D[2][3] = 30; D[2][4] = 30; D[2][5] = 25; D[2][6] = 25; D[2][7] = 20
D[3] = dict()
D[3][1] = 35; D[3][2] = 30; D[3][3] = 20; D[3][4] = 40; D[3][5] = 15; D[3][6] = 35; D[3][7] = 10
D[4] = dict()
D[4][1] = 30; D[4][2] = 45; D[4][3] = 35; D[4][4] = 25; D[4][5] = 30; D[4][6] = 20; D[4][7] = 25
D[5] = dict()
D[5][1] = 20; D[5][2] = 30; D[5][3] = 25; D[5][4] = 45; D[5][5] = 20; D[5][6] = 40; D[5][7] = 15
D[6] = dict()
D[6][1] = 40; D[6][2] = 25; D[6][3] = 30; D[6][4] = 20; D[6][5] = 35; D[6][6] = 15; D[6][7] = 30

# Machine hours a[m, j]
A = dict()
A[1] = dict()
A[1][1] = 0.5; A[1][2] = 0.7; A[1][3] = 0.0; A[1][4] = 0.0; A[1][5] = 0.3; A[1][6] = 0.2; A[1][7] = 0.5
A[2] = dict()
A[2][1] = 0.1; A[2][2] = 0.2; A[2][3] = 0.0; A[2][4] = 0.3; A[2][5] = 0.0; A[2][6] = 0.6; A[2][7] = 0.0
A[3] = dict()
A[3][1] = 0.2; A[3][2] = 0.0; A[3][3] = 0.8; A[3][4] = 0.0; A[3][5] = 0.0; A[3][6] = 0.0; A[3][7] = 0.6
A[4] = dict()
A[4][1] = 0.05; A[4][2] = 0.03; A[4][3] = 0.0; A[4][4] = 0.07; A[4][5] = 0.1; A[4][6] = 0.0; A[4][7] = 0.08
A[5] = dict()
A[5][1] = 0.0; A[5][2] = 0.0; A[5][3] = 0.01; A[5][4] = 0.0; A[5][5] = 0.05; A[5][6] = 0.0; A[5][7] = 0.05

# Capacity Cap[m, t]
Cap = dict()
Cap[1] = dict()
Cap[1][1] = 1152; Cap[1][2] = 1536; Cap[1][3] = 1536; Cap[1][4] = 1536; Cap[1][5] = 1152; Cap[1][6] = 1536
Cap[2] = dict()
Cap[2][1] = 768; Cap[2][2] = 768; Cap[2][3] = 768; Cap[2][4] = 384; Cap[2][5] = 384; Cap[2][6] = 768
Cap[3] = dict()
Cap[3][1] = 1152; Cap[3][2] = 384; Cap[3][3] = 1152; Cap[3][4] = 1152; Cap[3][5] = 1152; Cap[3][6] = 768
Cap[4] = dict()
Cap[4][1] = 384; Cap[4][2] = 384; Cap[4][3] = 0; Cap[4][4] = 384; Cap[4][5] = 384; Cap[4][6] = 384
Cap[5] = dict()
Cap[5][1] = 384; Cap[5][2] = 384; Cap[5][3] = 384; Cap[5][4] = 384; Cap[5][5] = 384; Cap[5][6] = 0

# Solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
I = dict()
for t in T:
    for j in J:
        x[t, j] = solver.NumVar(0, INF, 'x_' + str(t) + '_' + str(j))
        I[t, j] = solver.NumVar(0, H_max, 'I_' + str(t) + '_' + str(j))

# Objective: Maximize sum c_j * x_{t,j} - sum (c_j + h) * I_{t,j}
obj_terms = []
for t in T:
    for j in J:
        obj_terms.append(c[j] * x[t, j])
        obj_terms.append(-(c[j] + h) * I[t, j])
solver.Maximize(sum(obj_terms))

# Constraints
for t in T:
    for j in J:
        # Inventory balance: I_{t-1,j} + x_{t,j} - I_{t,j} = S_{t,j}
        # S between 0 and D[t][j]
        if t == 1:
            prev_I = 0
        else:
            prev_I = I[t - 1, j]

        # Sales >= 0: prev_I + x[t,j] - I[t,j] >= 0
        solver.Add(prev_I + x[t, j] - I[t, j] >= 0)
        # Sales <= Demand: prev_I + x[t,j] - I[t,j] <= D[t][j]
        solver.Add(prev_I + x[t, j] - I[t, j] <= D[t][j])

# Final inventory fix: I[6][j] = 50
for j in J:
    solver.Add(I[6, j] == 50)

# Machine capacity constraints
for t in T:
    for m in M:
        cap_expr = sum(A[m][j] * x[t, j] for j in J)
        solver.Add(cap_expr <= Cap[m][t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")