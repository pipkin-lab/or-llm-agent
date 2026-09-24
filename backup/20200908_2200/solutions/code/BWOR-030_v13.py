from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Parameters
C_cap = 5000
I_0 = 1000
K_0 = 20000
I_target = 2000

# Prices
PB = dict()
PS = dict()
PB[1] = 2.85
PB[2] = 3.05
PB[3] = 2.90
PS[1] = 3.10
PS[2] = 3.25
PS[3] = 2.95

# Decision variables
x = dict()
y = dict()
I = dict()
K = dict()

for t in range(1, 4):
    x[t] = solver.NumVar(0, inf, 'x_' + str(t))
    y[t] = solver.NumVar(0, inf, 'y_' + str(t))
    I[t] = solver.NumVar(0, inf, 'I_' + str(t))
    K[t] = solver.NumVar(0, inf, 'K_' + str(t))

# Constraints
prev_I = I_0
prev_K = K_0
for t in range(1, 4):
    # Inventory dynamics: I[t] = prev_I + x[t] - y[t]
    solver.Add(I[t] == prev_I + x[t] - y[t])
    # Sales limitation: y[t] <= prev_I
    solver.Add(y[t] <= prev_I)
    # Warehouse capacity
    solver.Add(I[t] <= C_cap)
    # Cash dynamics: K[t] = prev_K - PB[t]*x[t] + PS[t]*y[t]
    solver.Add(K[t] == prev_K - PB[t] * x[t] + PS[t] * y[t])
    # Update for next iteration
    prev_I = I[t]
    prev_K = K[t]

# Final inventory target
solver.Add(I[3] == I_target)

# Objective: Maximize K[3]
solver.Maximize(K[3])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")