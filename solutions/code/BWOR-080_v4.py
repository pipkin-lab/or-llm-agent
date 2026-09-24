from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index sets
J = list(range(1, 8))   # Products 1..7
T = list(range(1, 7))   # Months 1..6
M = list(range(1, 6))   # Machine types 1..5

# Parameters
p = dict()
p[1] = 100
p[2] = 60
p[3] = 80
p[4] = 40
p[5] = 110
p[6] = 90
p[7] = 30

h = dict()
for j in J:
    h[j] = 5

# Demand D[j][t]
D = dict()
D[1] = dict()
D[1][1] = 500
D[1][2] = 600
D[1][3] = 300
D[1][4] = 200
D[1][5] = 0
D[1][6] = 500
D[2] = dict()
D[2][1] = 1000
D[2][2] = 500
D[2][3] = 600
D[2][4] = 300
D[2][5] = 100
D[2][6] = 500
D[3] = dict()
D[3][1] = 300
D[3][2] = 200
D[3][3] = 0
D[3][4] = 400
D[3][5] = 500
D[3][6] = 100
D[4] = dict()
D[4][1] = 300
D[4][2] = 0
D[4][3] = 0
D[4][4] = 500
D[4][5] = 100
D[4][6] = 300
D[5] = dict()
D[5][1] = 800
D[5][2] = 400
D[5][3] = 500
D[5][4] = 200
D[5][5] = 1000
D[5][6] = 1100
D[6] = dict()
D[6][1] = 200
D[6][2] = 300
D[6][3] = 400
D[6][4] = 0
D[6][5] = 300
D[6][6] = 500
D[7] = dict()
D[7][1] = 100
D[7][2] = 150
D[7][3] = 100
D[7][4] = 100
D[7][5] = 0
D[7][6] = 60

# Capacity Cap[m][t]
Cap = dict()
Cap[1] = dict()
Cap[1][1] = 1152
Cap[1][2] = 1536
Cap[1][3] = 1536
Cap[1][4] = 1536
Cap[1][5] = 1152
Cap[1][6] = 1536
Cap[2] = dict()
Cap[2][1] = 768
Cap[2][2] = 768
Cap[2][3] = 768
Cap[2][4] = 384
Cap[2][5] = 384
Cap[2][6] = 768
Cap[3] = dict()
Cap[3][1] = 1152
Cap[3][2] = 384
Cap[3][3] = 1152
Cap[3][4] = 1152
Cap[3][5] = 1152
Cap[3][6] = 768
Cap[4] = dict()
Cap[4][1] = 384
Cap[4][2] = 384
Cap[4][3] = 0
Cap[4][4] = 384
Cap[4][5] = 384
Cap[4][6] = 384
Cap[5] = dict()
Cap[5][1] = 384
Cap[5][2] = 384
Cap[5][3] = 384
Cap[5][4] = 384
Cap[5][5] = 384
Cap[5][6] = 0

# Processing times a[m][j]
a = dict()
for m in M:
    for j in J:
        a[(m, j)] = 0

a[(1, 1)] = 0.5
a[(1, 2)] = 0.7
a[(1, 5)] = 0.3
a[(1, 6)] = 0.2
a[(1, 7)] = 0.5
a[(2, 1)] = 0.1
a[(2, 2)] = 0.2
a[(2, 4)] = 0.3
a[(2, 6)] = 0.6
a[(3, 1)] = 0.2
a[(3, 3)] = 0.8
a[(3, 7)] = 0.6
a[(4, 1)] = 0.05
a[(4, 2)] = 0.03
a[(4, 4)] = 0.07
a[(4, 5)] = 0.1
a[(4, 7)] = 0.08
a[(5, 3)] = 0.01
a[(5, 5)] = 0.05
a[(5, 7)] = 0.05

# Inventory bound
S_max = 100
I_final = 50

# Decision variables
x = dict()
s = dict()
I = dict()
for j in J:
    for t in T:
        x[(j, t)] = solver.IntVar(0, INF, 'x_' + str(j) + '_' + str(t))
        s[(j, t)] = solver.IntVar(0, D[j][t], 's_' + str(j) + '_' + str(t))
        I[(j, t)] = solver.IntVar(0, S_max, 'I_' + str(j) + '_' + str(t))

# Objective: maximize sum(p_j * s_jt) - sum(h_j * I_jt)
obj = 0
for t in T:
    for j in J:
        obj += p[j] * s[(j, t)]
        obj -= h[j] * I[(j, t)]

solver.Maximize(obj)

# Inventory balance: I[j,t-1] + x[j,t] - s[j,t] = I[j,t]
for t in T:
    for j in J:
        if t == 1:
            solver.Add(0 + x[(j, t)] - s[(j, t)] == I[(j, t)])
        else:
            solver.Add(I[(j, t - 1)] + x[(j, t)] - s[(j, t)] == I[(j, t)])

# Machine capacity constraints
for t in T:
    for m in M:
        expr = sum(a[(m, j)] * x[(j, t)] for j in J)
        solver.Add(expr <= Cap[m][t])

# Final inventory requirement
for j in J:
    solver.Add(I[(j, 6)] == I_final)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")