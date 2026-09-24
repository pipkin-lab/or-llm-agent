from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

T = range(1, 7)
K = range(1, 6)

D = dict()
D[1] = 40
D[2] = 20
D[3] = 30
D[4] = 40
D[5] = 30
D[6] = 20

q = dict()
q[1] = 10
q[2] = 20
q[3] = 30
q[4] = 40
q[5] = 50

C = dict()
C[1] = 48
C[2] = 86
C[3] = 118
C[4] = 138
C[5] = 160

F = 10
h = 0.2
I_max = 40

y = dict()
for t in T:
    for k in K:
        y[t, k] = solver.BoolVar('y_' + str(t) + '_' + str(k))

I = dict()
for t in T:
    I[t] = solver.NumVar(0, I_max, 'I_' + str(t))

# Objective
obj = 0
for t in T:
    for k in K:
        obj += F * y[t, k] + C[k] * y[t, k]
    obj += h * I[t]

solver.Minimize(obj)

# Single order constraint
for t in T:
    solver.Add(sum(y[t, k] for k in K) <= 1)

# Inventory balance
for t in T:
    order_qty = sum(q[k] * y[t, k] for k in K)
    if t == 1:
        solver.Add(I[t] == order_qty - D[t])
    else:
        solver.Add(I[t] == I[t - 1] + order_qty - D[t])

# End-of-season inventory
solver.Add(I[6] == 0)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")