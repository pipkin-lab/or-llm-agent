from ortools.linear_solver import pywraplp

# Parameters
T = 6
D = dict()
D[1] = 3000
D[2] = 3600
D[3] = 4000
D[4] = 4600
D[5] = 4800
D[6] = 5000

h_prod = 4
h_train = 50
c_m = 150
p_sell = 240
W0 = 80
H_month = 160
c_w = 2000
c_tr = 800
alpha = 0.02
I0 = 400
I_max = 100
c_s = 10

# Solver setup (MILP)
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
W = dict()
N = dict()
P = dict()
I = dict()

for t in range(1, T + 1):
    W[t] = solver.IntVar(0, INF, 'W_' + str(t))
    N[t] = solver.IntVar(0, INF, 'N_' + str(t))
    P[t] = solver.NumVar(0, INF, 'P_' + str(t))
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))

# Objective: maximize profit
obj = 0
for t in range(1, T + 1):
    obj += (p_sell - c_m) * P[t] - c_w * W[t] - c_tr * N[t] - c_s * I[t]

solver.Maximize(obj)

# Constraint 1a: W_1 = 80
solver.Add(W[1] == W0)

# Constraint 1b: Workforce balance for t = 2, ..., 6
# W_t = 0.98 * W_{t-1} + 0.02 * N_{t-2} + N_{t-1}
# where N_0 = 0
for t in range(2, T + 1):
    if t == 2:
        # N_0 = 0, so the 0.02 * N_0 term vanishes
        solver.Add(W[t] == 0.98 * W[t - 1] + N[t - 1])
    else:
        solver.Add(W[t] == 0.98 * W[t - 1] + 0.02 * N[t - 2] + N[t - 1])

# Constraint 2: Production capacity
for t in range(1, T + 1):
    solver.Add(h_prod * P[t] + h_train * N[t] <= H_month * W[t])

# Constraint 3: Inventory balance
for t in range(1, T + 1):
    if t == 1:
        solver.Add(I[t] == I0 + P[t] - D[t])
    else:
        solver.Add(I[t] == I[t - 1] + P[t] - D[t])

# Constraint 4: Ending inventory constraint
solver.Add(I[T] <= I_max)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")