from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Parameters
T = range(1, 7)
K = range(1, 6)

Q = dict()
Q[1] = 10
Q[2] = 20
Q[3] = 30
Q[4] = 40
Q[5] = 50

C_fixed = 10
C_var = dict()
C_var[1] = 48
C_var[2] = 86
C_var[3] = 118
C_var[4] = 138
C_var[5] = 160

h = 0.2

D = dict()
D[1] = 40
D[2] = 20
D[3] = 30
D[4] = 40
D[5] = 30
D[6] = 20

# Decision Variables
y = dict()
for t in T:
    for k in K:
        y[t, k] = solver.BoolVar('y_' + str(t) + '_' + str(k))

I = dict()
for t in T:
    I[t] = solver.NumVar(0, 40, 'I_' + str(t))

# Objective
obj = 0
for t in T:
    for k in K:
        obj += (C_fixed + C_var[k]) * y[t, k]
for t in T:
    obj += h * I[t]

solver.Minimize(obj)

# Constraints

# Inventory Balance
for t in T:
    if t == 1:
        prev_I = 0
    else:
        prev_I = I[t - 1]
    order_qty = sum(Q[k] * y[t, k] for k in K)
    solver.Add(prev_I + order_qty - D[t] == I[t])

# Seasonal Boundary: I_6 = 0 (I_0 = 0 handled in balance for t=1)
solver.Add(I[6] == 0)

# Order Quantity Constraints: at most one order per month
for t in T:
    solver.Add(sum(y[t, k] for k in K) <= 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")