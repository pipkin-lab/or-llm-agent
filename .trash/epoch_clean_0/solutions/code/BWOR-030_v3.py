from ortools.linear_solver import pywraplp

# Initialize solver (LP since all variables are continuous)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
C_wh = 5000
I_0 = 1000
K_0 = 20000
I_target = 2000

p = {1: 2.85, 2: 3.05, 3: 2.90}
s = {1: 3.10, 2: 3.25, 3: 2.95}

# Decision Variables
x = dict()
y = dict()
I = dict()

for t in range(1, 4):
    x[t] = solver.NumVar(0, solver.infinity(), 'x_' + str(t))
    y[t] = solver.NumVar(0, solver.infinity(), 'y_' + str(t))
    I[t] = solver.NumVar(0, solver.infinity(), 'I_' + str(t))

# Objective Function: Maximize Profit
obj = 0
for t in range(1, 4):
    obj += s[t] * y[t] - p[t] * x[t]
solver.Maximize(obj)

# A. Inventory Balance Constraints
# I_1 = 1000 + x_1 - y_1
solver.Add(I[1] == I_0 + x[1] - y[1])
# I_2 = I_1 + x_2 - y_2
solver.Add(I[2] == I[1] + x[2] - y[2])
# I_3 = I_2 + x_3 - y_3
solver.Add(I[3] == I[2] + x[3] - y[3])

# B. Warehouse Capacity Constraints
for t in range(1, 4):
    solver.Add(I[t] <= C_wh)

# C. Target Ending Inventory Constraint
solver.Add(I[3] == I_target)

# D. Sales Feasibility Constraints (Lag Constraint)
# y_1 <= 1000
solver.Add(y[1] <= I_0)
# y_2 <= I_1
solver.Add(y[2] <= I[1])
# y_3 <= I_2
solver.Add(y[3] <= I[2])

# E. Cash Flow / Capital Constraints (Start of Month)
# 1. 2.85 x_1 <= 20000
solver.Add(2.85 * x[1] <= K_0)

# 2. 3.05 x_2 <= 20000 - 2.85 x_1 + 3.10 y_1
#    2.85 x_1 + 3.05 x_2 - 3.10 y_1 <= 20000
solver.Add(2.85 * x[1] + 3.05 * x[2] - 3.10 * y[1] <= K_0)

# 3. 2.90 x_3 <= 20000 - 2.85 x_1 + 3.10 y_1 - 3.05 x_2 + 3.25 y_2
#    2.85 x_1 + 3.05 x_2 + 2.90 x_3 - 3.10 y_1 - 3.25 y_2 <= 20000
solver.Add(2.85 * x[1] + 3.05 * x[2] + 2.90 * x[3] - 3.10 * y[1] - 3.25 * y[2] <= K_0)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")