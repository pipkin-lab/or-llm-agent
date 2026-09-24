from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
T = 6
K_list = list(range(6))  # k = 0 to 5
Q = dict()
Q[0] = 0
Q[1] = 10
Q[2] = 20
Q[3] = 30
Q[4] = 40
Q[5] = 50

K_cost = dict()
K_cost[0] = 0
K_cost[1] = 58
K_cost[2] = 96
K_cost[3] = 128
K_cost[4] = 148
K_cost[5] = 170

D = dict()
D[1] = 40
D[2] = 20
D[3] = 30
D[4] = 40
D[5] = 30
D[6] = 20

h = 0.2
I_max = 40

# Decision variables
x = dict()
for t in range(1, T + 1):
    for k in K_list:
        x[t, k] = solver.BoolVar('x_' + str(t) + '_' + str(k))

I = dict()
for t in range(1, T + 1):
    I[t] = solver.NumVar(0, I_max, 'I_' + str(t))

# Constraints

# 1. Exactly one order option per month
for t in range(1, T + 1):
    solver.Add(sum(x[t, k] for k in K_list) == 1)

# 2. Inventory balance
for t in range(1, T + 1):
    order_qty = sum(Q[k] * x[t, k] for k in K_list)
    if t == 1:
        prev_I = 0
    else:
        prev_I = I[t - 1]
    solver.Add(I[t] == prev_I + order_qty - D[t])

# 3. Final inventory constraint
solver.Add(I[6] == 0)

# 4. Inventory capacity (already bounded by NumVar, but I_t <= 40 for t=1..5 is explicit)
# The bounds are already set in NumVar(0, I_max, ...), so no additional constraint needed for I_t <= 40

# Objective
obj = 0
for t in range(1, T + 1):
    for k in K_list:
        obj += K_cost[k] * x[t, k]
    obj += h * I[t]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")