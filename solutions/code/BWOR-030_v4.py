from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
C_cap = 5000
S0 = 1000
K0 = 20000
S_end = 2000

P = dict()
R = dict()
P[1] = 2.85
P[2] = 3.05
P[3] = 2.90
R[1] = 3.10
R[2] = 3.25
R[3] = 2.95

T = [1, 2, 3]

# Decision variables
x = dict()
y = dict()
I = dict()
K = dict()

for t in T:
    x[t] = solver.NumVar(0, INF, 'x_' + str(t))
    y[t] = solver.NumVar(0, INF, 'y_' + str(t))
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))
    K[t] = solver.NumVar(0, INF, 'K_' + str(t))

# Inventory dynamics
solver.Add(I[1] == S0 + x[1] - y[1])
solver.Add(I[2] == I[1] + x[2] - y[2])
solver.Add(I[3] == I[2] + x[3] - y[3])

# Sales availability (lagged sales)
solver.Add(y[1] <= S0)
solver.Add(y[2] <= I[1])
solver.Add(y[3] <= I[2])

# Warehouse capacity
for t in T:
    solver.Add(I[t] <= C_cap)

# Cash flow
solver.Add(K[1] == K0 + R[1] * y[1] - P[1] * x[1])
solver.Add(K[2] == K[1] + R[2] * y[2] - P[2] * x[2])
solver.Add(K[3] == K[2] + R[3] * y[3] - P[3] * x[3])

# Target end inventory
solver.Add(I[3] == S_end)

# Objective: maximize final cash balance
solver.Maximize(K[3])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")