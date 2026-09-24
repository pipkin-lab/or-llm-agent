from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

months = [1, 2, 3, 4]

P_buy = dict()
P_buy[1] = 10
P_buy[2] = 9
P_buy[3] = 11
P_buy[4] = 15

P_sell = dict()
P_sell[1] = 12
P_sell[2] = 9
P_sell[3] = 13
P_sell[4] = 17

x = dict()
y = dict()
I = dict()

for k in months:
    x[k] = solver.IntVar(0, INF, 'x_' + str(k))
    y[k] = solver.IntVar(0, INF, 'y_' + str(k))
    I[k] = solver.IntVar(0, 1000, 'I_' + str(k))

# Inventory balance constraints
solver.Add(I[1] == 500 - y[1])
solver.Add(I[2] == I[1] + x[1] - y[2])
solver.Add(I[3] == I[2] + x[2] - y[3])
solver.Add(I[4] == I[3] + x[3] - y[4])

# Sales feasibility constraints (redundant given I>=0 and balance, but explicit per model)
solver.Add(y[1] <= 500)
solver.Add(y[2] <= I[1] + x[1])
solver.Add(y[3] <= I[2] + x[2])
solver.Add(y[4] <= I[3] + x[3])

# Objective: maximize total profit
obj = 0
for k in months:
    obj += P_sell[k] * y[k] - P_buy[k] * x[k]

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")