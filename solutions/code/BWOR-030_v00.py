from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
P = dict()
S = dict()
for t in range(1, 4):
    P[t] = solver.NumVar(0, INF, 'P_' + str(t))
    S[t] = solver.NumVar(0, INF, 'S_' + str(t))

# Inventory variables
I = dict()
for t in range(1, 4):
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))

# Parameters
I0 = 1000
I3_target = 2000
capacity = 5000
initial_cash = 20000

buy_price = {1: 2.85, 2: 3.05, 3: 2.90}
sell_price = {1: 3.10, 2: 3.25, 3: 2.95}

# Inventory balance constraints
solver.Add(I[1] == I0 + P[1] - S[1])
solver.Add(I[2] == I[1] + P[2] - S[2])
solver.Add(I[3] == I[2] + P[3] - S[3])

# Target end-of-month-3 inventory
solver.Add(I[3] == I3_target)

# Warehouse capacity constraints
for t in range(1, 4):
    solver.Add(I[t] <= capacity)

# Sales timing constraints
solver.Add(S[1] <= I0)
solver.Add(S[2] <= I[1])
solver.Add(S[3] <= I[2])

# Financial constraints
# Beginning of Month 1: 2.85 * P1 <= 20000
solver.Add(buy_price[1] * P[1] <= initial_cash)

# Beginning of Month 2: 3.05 * P2 <= C1 - 2.85*P1 + 3.10*S1
C2_expr = initial_cash - buy_price[1] * P[1] + sell_price[1] * S[1]
solver.Add(buy_price[2] * P[2] <= C2_expr)

# Beginning of Month 3: 2.90 * P3 <= C2 - 3.05*P2 + 3.25*S2
C3_expr = C2_expr - buy_price[2] * P[2] + sell_price[2] * S[2]
solver.Add(buy_price[3] * P[3] <= C3_expr)

# Objective: Maximize total profit
obj = sum(sell_price[t] * S[t] - buy_price[t] * P[t] for t in range(1, 4))
solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")