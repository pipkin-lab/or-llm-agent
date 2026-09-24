from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index set
months = [1, 2, 3, 4, 5, 6]
n = len(months)

# Parameters
D = dict()
D[1] = 3000
D[2] = 3600
D[3] = 4000
D[4] = 4600
D[5] = 4800
D[6] = 5000

I0 = 400
S0 = 80
c_sk = 2000
c_tr = 800
c_mat = 150
p_sell = 240
c_store = 10
h_prod = 4
h_train = 50
H_cap = 160
alpha = 0.02
I_max_6 = 100

# Variables
S = dict()
H = dict()
A = dict()
x = dict()
I = dict()

for t in months:
    S[t] = solver.IntVar(0, INF, 'S_' + str(t))
    H[t] = solver.IntVar(0, INF, 'H_' + str(t))
    A[t] = solver.IntVar(0, INF, 'A_' + str(t))
    x[t] = solver.IntVar(0, INF, 'x_' + str(t))
    I[t] = solver.IntVar(0, INF, 'I_' + str(t))

# Constraints

# 1. Workforce Balance
# S_1 = 80
solver.Add(S[1] == S0)

# For t in 2..6: S_t = S_{t-1} - A_{t-1} + H_{t-1}
for t in months:
    if t > 1:
        solver.Add(S[t] == S[t - 1] - A[t - 1] + H[t - 1])

# 2. Attrition Logic
# For each t in 1..6:
# A_t >= alpha * S_t
# A_t <= alpha * S_t + 1
for t in months:
    solver.Add(A[t] >= alpha * S[t])
    solver.Add(A[t] <= alpha * S[t] + 1)

# 3. Labor Capacity
# For t in 1..6: 4*x_t + 50*H_t <= 160*S_t
for t in months:
    solver.Add(h_prod * x[t] + h_train * H[t] <= H_cap * S[t])

# 4. Inventory Balance
# I_t = I_{t-1} + x_t - D_t
# I_0 = 400
for t in months:
    if t == 1:
        solver.Add(I[t] == I0 + x[t] - D[t])
    else:
        solver.Add(I[t] == I[t - 1] + x[t] - D[t])

# 5. Inventory Limits
# I_6 <= 100
solver.Add(I[6] <= I_max_6)

# Objective: Maximize Net Profit
# Z = sum_{t=1..6} (90*x_t - 2000*S_t - 800*H_t - 10*I_t)
obj_terms = []
for t in months:
    obj_terms.append((p_sell - c_mat) * x[t] - c_sk * S[t] - c_tr * H[t] - c_store * I[t])

objective = sum(obj_terms)
solver.Maximize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")