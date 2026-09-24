from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
p = dict()
s = dict()
D = dict()
p[1] = 410
p[2] = 430
p[3] = 460
p[4] = 450
s[1] = 425
s[2] = 440
s[3] = 465
s[4] = 455
D[1] = 100
D[2] = 140
D[3] = 200
D[4] = 160
K = 20
a = 70
b = 100

# Decision variables
x = dict()
z = dict()
y = dict()
I = dict()

for t in range(1, 5):
    x[t] = solver.NumVar(0, INF, 'x_' + str(t))
    z[t] = solver.NumVar(0, INF, 'z_' + str(t))
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))

# y[i,j] for 1 <= i < j <= 4
pairs = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
for (i, j) in pairs:
    y[i, j] = solver.NumVar(0, INF, 'y_' + str(i) + '_' + str(j))

# Objective function (consolidated)
obj = 0
obj += 15 * z[1] + 10 * z[2] + 5 * z[3] + 5 * z[4]
obj += -140 * y[1, 2] - 215 * y[1, 3] - 325 * y[1, 4]
obj += -135 * y[2, 3] - 245 * y[2, 4] - 175 * y[3, 4]

solver.Maximize(obj)

# Purchase-flow balance
# x1 = z1 + y12 + y13 + y14
solver.Add(x[1] == z[1] + y[1, 2] + y[1, 3] + y[1, 4])
# x2 = z2 + y23 + y24
solver.Add(x[2] == z[2] + y[2, 3] + y[2, 4])
# x3 = z3 + y34
solver.Add(x[3] == z[3] + y[3, 4])
# x4 = z4
solver.Add(x[4] == z[4])

# Sales volume constraints
# z1 <= D1
solver.Add(z[1] <= D[1])
# z2 + y12 <= D2
solver.Add(z[2] + y[1, 2] <= D[2])
# z3 + y13 + y23 <= D3
solver.Add(z[3] + y[1, 3] + y[2, 3] <= D[3])
# z4 + y14 + y24 + y34 <= D4
solver.Add(z[4] + y[1, 4] + y[2, 4] + y[3, 4] <= D[4])

# Warehouse capacity constraints
# I1 = y12 + y13 + y14
solver.Add(I[1] == y[1, 2] + y[1, 3] + y[1, 4])
# I2 = y13 + y14 + y23 + y24
solver.Add(I[2] == y[1, 3] + y[1, 4] + y[2, 3] + y[2, 4])
# I3 = y14 + y24 + y34
solver.Add(I[3] == y[1, 4] + y[2, 4] + y[3, 4])
# I4 = 0
solver.Add(I[4] == 0)

# Capacity bounds
for t in range(1, 5):
    solver.Add(I[t] <= K)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")