from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Parameters
T = [1, 2, 3, 4, 5, 6]
D = dict()
D[1] = 3000
D[2] = 3600
D[3] = 4000
D[4] = 4600
D[5] = 4800
D[6] = 5000

W1 = 80
I0 = 400
Imax_end = 100
c_price = 240
c_mat = 150
c_wage = 2000
c_train = 800
c_store = 10
r_attr = 0.02
H_cap = 160
h_unit = 4
h_train = 50

# Variables
W = dict()
Tr = dict()
P = dict()
S = dict()
I = dict()

for t in T:
    W[t] = solver.NumVar(0, INF, 'W_' + str(t))
    Tr[t] = solver.IntVar(0, INF, 'T_' + str(t))
    P[t] = solver.NumVar(0, INF, 'P_' + str(t))
    S[t] = solver.NumVar(0, INF, 'S_' + str(t))
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))

# Constraints

# Workforce initial condition
solver.Add(W[1] == W1)

# Workforce balance for t=1..5
for t in [1, 2, 3, 4, 5]:
    tp1 = t + 1
    solver.Add(W[tp1] == (1 - r_attr) * W[t] + Tr[t])

# Production capacity for all t
for t in T:
    solver.Add(h_unit * P[t] + h_train * Tr[t] <= H_cap * W[t])

# Inventory balance for all t
for t in T:
    if t == 1:
        solver.Add(I[t] == I0 + P[t] - S[t])
    else:
        tm1 = t - 1
        solver.Add(I[t] == I[tm1] + P[t] - S[t])

# Demand constraints
for t in T:
    solver.Add(S[t] <= D[t])

# Ending inventory constraint
solver.Add(I[6] <= Imax_end)

# Objective: Maximize Profit
obj_terms = []
for t in T:
    obj_terms.append(c_price * S[t])
    obj_terms.append(-c_wage * W[t])
    obj_terms.append(-c_train * Tr[t])
    obj_terms.append(-c_mat * P[t])
    obj_terms.append(-c_store * I[t])

objective = sum(obj_terms)
solver.Maximize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")