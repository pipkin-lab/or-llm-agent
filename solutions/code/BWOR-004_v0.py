from ortools.linear_solver import pywraplp

# Parameters
T = [1, 2, 3, 4, 5, 6]
D = {1: 3000, 2: 3600, 3: 4000, 4: 4600, 5: 4800, 6: 5000}
h_L = 4
c_M = 150
P_sell = 240
H_mon = 160
W_start = 80
h_train = 50
c_S = 2000
c_T = 800
r = 0.02
I_start = 400
I_max = 100
c_H = 10

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Variables
W = dict()
Y = dict()
A = dict()
P = dict()
I = dict()

for t in T:
    W[t] = solver.IntVar(0, INF, 'W_' + str(t))
    Y[t] = solver.IntVar(0, INF, 'Y_' + str(t))
    P[t] = solver.NumVar(0, INF, 'P_' + str(t))
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))

for t in [1, 2, 3, 4, 5]:
    A[t] = solver.IntVar(0, INF, 'A_' + str(t))

# Constraints
# 1. Initial workforce
solver.Add(W[1] == W_start)

# 2. Workforce balance for t = 1 to 5
for t in [1, 2, 3, 4, 5]:
    solver.Add(W[t + 1] == W[t] - A[t] + Y[t])
    # 3. Attrition constraint
    solver.Add(A[t] >= r * W[t])

# 4. Production capacity for each month
for t in T:
    solver.Add(h_L * P[t] <= H_mon * W[t] - h_train * Y[t])

# 5. Inventory balance for each month
for t in T:
    if t == 1:
        solver.Add(I[t] == I_start + P[t] - D[t])
    else:
        solver.Add(I[t] == I[t - 1] + P[t] - D[t])

# 8. Ending inventory constraint
solver.Add(I[6] <= I_max)

# Objective: Maximize Profit
# Profit = sum(240*D[t]) - sum(150*P[t] + 2000*W[t] + 800*Y[t] + 10*I[t])
# Since sum(240*D[t]) is constant, we can maximize:
# -sum(150*P[t] + 2000*W[t] + 800*Y[t] + 10*I[t])
# Or equivalently minimize the cost part. Let's maximize profit directly.
constant_revenue = sum(P_sell * D[t] for t in T)
cost_terms = []
for t in T:
    cost_terms.append(c_M * P[t])
    cost_terms.append(c_S * W[t])
    cost_terms.append(c_T * Y[t])
    cost_terms.append(c_H * I[t])

total_cost = sum(cost_terms)
# Maximize Profit = constant_revenue - total_cost
# This is equivalent to Minimize total_cost
solver.Minimize(total_cost)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    optimal_profit = constant_revenue - solver.Objective().Value()
    print("OPTIMAL_VALUE:", optimal_profit)
else:
    print("NO_FEASIBLE_SOLUTION")