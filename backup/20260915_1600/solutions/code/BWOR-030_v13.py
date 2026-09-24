from ortools.linear_solver import pywraplp

# Parameters
C_max = 5000
I_0 = 1000
K_0 = 20000
I_end = 2000

P = dict()
P[1] = 2.85
P[2] = 3.05
P[3] = 2.90

S = dict()
S[1] = 3.10
S[2] = 3.25
S[3] = 2.95

months = [1, 2, 3]

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
y = dict()
I = dict()
K = dict()

for t in months:
    x[t] = solver.NumVar(0, INF, 'x_' + str(t))
    y[t] = solver.NumVar(0, INF, 'y_' + str(t))
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))
    K[t] = solver.NumVar(0, INF, 'K_' + str(t))

# Inventory balance constraints
# I_1 = I_0 + x_1 - y_1
solver.Add(I[1] == I_0 + x[1] - y[1])
# I_2 = I_1 + x_2 - y_2
solver.Add(I[2] == I[1] + x[2] - y[2])
# I_3 = I_2 + x_3 - y_3
solver.Add(I[3] == I[2] + x[3] - y[3])

# Warehouse capacity constraints
solver.Add(I[1] <= C_max)
solver.Add(I[2] <= C_max)

# Target ending inventory constraint
solver.Add(I[3] == I_end)

# Sales timing constraints
# y_1 can only come from initial stock
solver.Add(y[1] <= I_0)
# y_2 can come from inventory at end of month 1 (which is I_0 + x_1 - y_1)
# But more precisely, available for sale in month 2 is inventory at beginning of month 2 = I_1
# However, the model states y_2 <= I_1 and y_3 <= I_2
solver.Add(y[2] <= I[1])
solver.Add(y[3] <= I[2])

# Cash flow / capital constraints
# K_1 = K_0 + S_1 * y_1 - P_1 * x_1
solver.Add(K[1] == K_0 + S[1] * y[1] - P[1] * x[1])
# K_2 = K_1 + S_2 * y_2 - P_2 * x_2
solver.Add(K[2] == K[1] + S[2] * y[2] - P[2] * x[2])
# K_3 = K_2 + S_3 * y_3 - P_3 * x_3
solver.Add(K[3] == K[2] + S[3] * y[3] - P[3] * x[3])

# Objective: Maximize K_3
solver.Maximize(K[3])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")