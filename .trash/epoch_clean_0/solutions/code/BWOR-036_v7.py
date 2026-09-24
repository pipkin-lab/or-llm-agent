from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
p = dict()
p[1] = 410
p[2] = 430
p[3] = 460
p[4] = 450

s = dict()
s[1] = 425
s[2] = 440
s[3] = 465
s[4] = 455

D = dict()
D[1] = 100
D[2] = 140
D[3] = 200
D[4] = 160

C_cap = 20
a = 0.07
b = 0.1

# Decision variables
x = dict()
y = dict()
v = dict()
z = dict()
w = dict()

for t in range(1, 5):
    x[t] = solver.NumVar(0, INF, 'x_' + str(t))
    y[t] = solver.NumVar(0, INF, 'y_' + str(t))
    v[t] = solver.NumVar(0, INF, 'v_' + str(t))

for t in range(1, 4):
    z[t] = solver.NumVar(0, INF, 'z_' + str(t))

# w[t, k]: purchased in t, stored for k quarters (sold in t+k)
# Valid pairs:
# t=1: k in 1,2,3
# t=2: k in 1,2
# t=3: k in 1
w[1, 1] = solver.NumVar(0, INF, 'w_1_1')
w[1, 2] = solver.NumVar(0, INF, 'w_1_2')
w[1, 3] = solver.NumVar(0, INF, 'w_1_3')
w[2, 1] = solver.NumVar(0, INF, 'w_2_1')
w[2, 2] = solver.NumVar(0, INF, 'w_2_2')
w[3, 1] = solver.NumVar(0, INF, 'w_3_1')

# Objective: maximize profit
obj = 0
for t in range(1, 5):
    obj += s[t] * y[t] - p[t] * x[t]

# Storage cost for w[t, k]
storage_cost_pairs = dict()
storage_cost_pairs[(1, 1)] = a + b * 1
storage_cost_pairs[(1, 2)] = a + b * 2
storage_cost_pairs[(1, 3)] = a + b * 3
storage_cost_pairs[(2, 1)] = a + b * 1
storage_cost_pairs[(2, 2)] = a + b * 2
storage_cost_pairs[(3, 1)] = a + b * 1

for (t, k), cost in storage_cost_pairs.items():
    obj -= cost * w[t, k]

solver.Maximize(obj)

# Constraint A: x_t = v_t + sum_k w[t,k]
for t in range(1, 5):
    expr = v[t]
    for k in range(1, 5 - t):
        expr += w[t, k]
    solver.Add(x[t] == expr)

# Constraint B: y_t = v_t + sum_{i=1}^{t-1} w[i, t-i]
for t in range(1, 5):
    expr = v[t]
    for i in range(1, t):
        expr += w[i, t - i]
    solver.Add(y[t] == expr)

# Constraint C: z_t = sum_{i=1}^{t-1} sum_{k=t-i+1}^{4-i} w[i, k]
for t in range(1, 4):
    expr = 0
    for i in range(1, t):
        for k in range(t - i + 1, 5 - i):
            expr += w[i, k]
    solver.Add(z[t] == expr)

# Constraint D: z_t <= C_cap
for t in range(1, 4):
    solver.Add(z[t] <= C_cap)

# Constraint E: y_t <= D_t
for t in range(1, 5):
    solver.Add(y[t] <= D[t])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")