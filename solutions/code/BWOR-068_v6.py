from ortools.linear_solver import pywraplp

# Parameters
T = [1, 2, 3, 4, 5, 6]
K = [1, 2, 3, 4, 5]

D = dict()
D[1] = 40
D[2] = 20
D[3] = 30
D[4] = 40
D[5] = 30
D[6] = 20

Q = dict()
Q[1] = 10
Q[2] = 20
Q[3] = 30
Q[4] = 40
Q[5] = 50

C = dict()
C[1] = 48
C[2] = 86
C[3] = 118
C[4] = 138
C[5] = 160

F = 10
h = 0.2
H_max = 40

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision Variables
x = dict()
for t in T:
    for k in K:
        x[t, k] = solver.BoolVar('x_' + str(t) + '_' + str(k))

I = dict()
for t in T:
    I[t] = solver.NumVar(0, H_max, 'I_' + str(t))

# Constraints

# A. One order per month (at most one)
for t in T:
    solver.Add(sum(x[t, k] for k in K) <= 1)

# B. Inventory Balance
for t in T:
    order_qty = sum(Q[k] * x[t, k] for k in K)
    if t == 1:
        solver.Add(I[t] == order_qty - D[t])
    else:
        solver.Add(I[t] == I[t - 1] + order_qty - D[t])

# C. Inventory Capacity (already bounded by NumVar upper bound, but add for clarity)
for t in T:
    solver.Add(I[t] <= H_max)

# D. Non-Backlogging (already bounded by NumVar lower bound of 0)

# E. End-of-Season Constraint
solver.Add(I[6] == 0)

# Objective Function
obj = 0
for t in T:
    for k in K:
        obj += C[k] * x[t, k]
    obj += F * sum(x[t, k] for k in K)
    obj += h * I[t]

solver.Minimize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")