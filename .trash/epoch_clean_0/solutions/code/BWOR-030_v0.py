from ortools.linear_solver import pywraplp

# Initialize solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
Cap = 5000
I_init = 1000
I_end = 2000
C_init = 20000

# Purchase prices (yuan/dan)
c = [2.85, 3.05, 2.90]
# Selling prices (yuan/dan)
r = [3.10, 3.25, 2.95]

T = 3

# Decision Variables
x = dict()
y = dict()
I = dict()
K = dict()

for t in range(T):
    x[t] = solver.NumVar(0, solver.infinity(), 'x_' + str(t))
    y[t] = solver.NumVar(0, solver.infinity(), 'y_' + str(t))
    I[t] = solver.NumVar(0, Cap, 'I_' + str(t))
    K[t] = solver.NumVar(0, solver.infinity(), 'K_' + str(t))

# Inventory Balance Constraints
# I_1 = I_0 + x_1 - y_1
solver.Add(I[0] == I_init + x[0] - y[0])
# I_2 = I_1 + x_2 - y_2
solver.Add(I[1] == I[0] + x[1] - y[1])
# I_3 = I_2 + x_3 - y_3
solver.Add(I[2] == I[1] + x[2] - y[2])

# Target Ending Inventory
solver.Add(I[2] == I_end)

# Sales Constraints (Lag): y_t <= I_{t-1}
# y_1 <= I_0 = 1000
solver.Add(y[0] <= I_init)
# y_2 <= I_1
solver.Add(y[1] <= I[0])
# y_3 <= I_2
solver.Add(y[2] <= I[1])

# Cash Flow Constraints
# K_1 = K_0 - c_1*x_1 + r_1*y_1
solver.Add(K[0] == C_init - c[0] * x[0] + r[0] * y[0])
# K_2 = K_1 - c_2*x_2 + r_2*y_2
solver.Add(K[1] == K[0] - c[1] * x[1] + r[1] * y[1])
# K_3 = K_2 - c_3*x_3 + r_3*y_3
solver.Add(K[2] == K[1] - c[2] * x[2] + r[2] * y[2])

# Objective Function: Maximize Total Profit
obj = sum(r[t] * y[t] - c[t] * x[t] for t in range(T))
solver.Maximize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")