from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
P_buy = {1: 2.85, 2: 3.05, 3: 2.90}
P_sell = {1: 3.10, 2: 3.25, 3: 2.95}
C_cap = 5000
I_0 = 1000
K_0 = 20000
I_target = 2000

# Decision variables
x = dict()
s = dict()
for t in [1, 2, 3]:
    x[t] = solver.NumVar(0, INF, 'x_' + str(t))
    s[t] = solver.NumVar(0, INF, 's_' + str(t))

# Objective: Maximize total profit
objective = 0
for t in [1, 2, 3]:
    objective += P_sell[t] * s[t] - P_buy[t] * x[t]
solver.Maximize(objective)

# Constraint 1: Target ending inventory
# sum(x) - sum(s) = 1000
solver.Add(sum(x[t] for t in [1, 2, 3]) - sum(s[t] for t in [1, 2, 3]) == 1000)

# Constraint 2: Warehouse capacity
# I_1 = 1000 + x_1 - s_1 <= 5000
solver.Add(1000 + x[1] - s[1] <= 5000)
# I_2 = 1000 + x_1 + x_2 - s_1 - s_2 <= 5000
solver.Add(1000 + x[1] + x[2] - s[1] - s[2] <= 5000)
# I_3 is fixed at 2000 by the target constraint, so I_3 <= 5000 is automatically satisfied.

# Constraint 3: Cash flow
# K_1 = 20000 + 3.10*s_1 - 2.85*x_1 >= 0
solver.Add(20000 + 3.10 * s[1] - 2.85 * x[1] >= 0)
# K_2 = K_1 + 3.25*s_2 - 3.05*x_2 >= 0
# 20000 + 3.10*s_1 - 2.85*x_1 + 3.25*s_2 - 3.05*x_2 >= 0
solver.Add(20000 + 3.10 * s[1] - 2.85 * x[1] + 3.25 * s[2] - 3.05 * x[2] >= 0)
# K_3 = K_2 + 2.95*s_3 - 2.90*x_3 >= 0
# 20000 + 3.10*s_1 - 2.85*x_1 + 3.25*s_2 - 3.05*x_2 + 2.95*s_3 - 2.90*x_3 >= 0
solver.Add(20000 + 3.10 * s[1] - 2.85 * x[1] + 3.25 * s[2] - 3.05 * x[2] + 2.95 * s[3] - 2.90 * x[3] >= 0)

# Constraint 4: Sales availability (time-lag constraints)
# s_1 <= 1000
solver.Add(s[1] <= 1000)
# s_2 <= 1000 + x_1
solver.Add(s[2] <= 1000 + x[1])
# s_3 <= 1000 + x_1 + x_2
solver.Add(s[3] <= 1000 + x[1] + x[2])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")