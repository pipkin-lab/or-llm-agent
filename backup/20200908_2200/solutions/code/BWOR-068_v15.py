from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
T = 6  # Months 1 to 6
K = 6  # Options 0 to 5

D = [40, 20, 30, 40, 30, 20]  # Demand for months 1 to 6 (index 0 to 5)
Q = [0, 10, 20, 30, 40, 50]   # Order quantities for options 0 to 5
C_var = [0, 48, 86, 118, 138, 160]  # Variable ordering costs
F_fixed = 10
H = 0.2
I_max = 40

# Decision Variables
x = dict()  # x[t, k] for t in 0..5, k in 0..5
for t in range(T):
    for k in range(K):
        x[t, k] = solver.BoolVar('x_' + str(t) + '_' + str(k))

I = dict()  # I[t] for t in 0..5 (end of month inventory)
for t in range(T):
    I[t] = solver.IntVar(0, I_max, 'I_' + str(t))

# Objective Function
obj = 0
for t in range(T):
    for k in range(K):
        cost_k = C_var[k]
        if k > 0:
            cost_k += F_fixed
        obj += cost_k * x[t, k]
    obj += H * I[t]

solver.Minimize(obj)

# Constraints

# 1. Order Selection: Exactly one option per month
for t in range(T):
    solver.Add(sum(x[t, k] for k in range(K)) == 1)

# 2. Inventory Balance
# I_t = I_{t-1} + sum(Q_k * x_{t,k}) - D_t
# I_0 = 0 is given. We define I[t] as end of month t+1 in 1-based, or t in 0-based.
# Let's be careful with indexing.
# I[t] is end of month t+1 (since t is 0-indexed).
# Beginning inventory for month t+1 is I[t-1] (or 0 if t=0).
for t in range(T):
    order_qty = sum(Q[k] * x[t, k] for k in range(K))
    if t == 0:
        solver.Add(I[t] == 0 + order_qty - D[t])
    else:
        solver.Add(I[t] == I[t - 1] + order_qty - D[t])

# 3. Inventory Capacity (already in variable bounds: I[t] <= 40)

# 4. Final Inventory Constraint: I_6 = 0 (end of month 6, which is index 5)
solver.Add(I[5] == 0)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")