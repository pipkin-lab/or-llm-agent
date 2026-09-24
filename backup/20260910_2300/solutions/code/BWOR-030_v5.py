from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    raise ValueError("GLOP solver not available")

INF = solver.infinity()

# Parameters
T = [1, 2, 3]
K = 5000
I0 = 1000
C0 = 20000
I_target = 2000

P_buy = dict()
P_sell = dict()
P_buy[1] = 2.85
P_buy[2] = 3.05
P_buy[3] = 2.90
P_sell[1] = 3.10
P_sell[2] = 3.25
P_sell[3] = 2.95

# Decision variables
x = dict()
y = dict()
I = dict()
C = dict()

for t in T:
    x[t] = solver.NumVar(0, INF, 'x_' + str(t))
    y[t] = solver.NumVar(0, INF, 'y_' + str(t))
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))
    C[t] = solver.NumVar(0, INF, 'C_' + str(t))

# Inventory balance
solver.Add(I[1] == I0 - y[1] + x[1])
solver.Add(I[2] == I[1] - y[2] + x[2])
solver.Add(I[3] == I[2] - y[3] + x[3])

# Sale timing (no same-month sale of new stock)
solver.Add(y[1] <= I0)
solver.Add(y[2] <= I[1])
solver.Add(y[3] <= I[2])

# Warehouse capacity
for t in T:
    solver.Add(I[t] <= K)

# Target end inventory
solver.Add(I[3] == I_target)

# Cash flow
solver.Add(C[1] == C0 - P_buy[1] * x[1] + P_sell[1] * y[1])
solver.Add(C[2] == C[1] - P_buy[2] * x[2] + P_sell[2] * y[2])
solver.Add(C[3] == C[2] - P_buy[3] * x[3] + P_sell[3] * y[3])

# Objective: maximize profit
obj = 0
for t in T:
    obj += P_sell[t] * y[t] - P_buy[t] * x[t]

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")