from ortools.linear_solver import pywraplp

# Parameters
T = range(1, 7)  # Months 1 through 6
U = 400          # Monthly production capacity
W = 300          # Warehouse storage capacity
c = 100          # Variable production cost (yuan/unit)
F = 4000         # Fixed production cost (yuan)
h = 10           # Holding cost (yuan/unit/month)
d = dict()
d[1] = 100
d[2] = 200
d[3] = 500
d[4] = 300
d[5] = 200
d[6] = 100

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision Variables
P = dict()
I = dict()
y = dict()
for t in T:
    P[t] = solver.NumVar(0, U, 'P_' + str(t))
    I[t] = solver.NumVar(0, W, 'I_' + str(t))
    y[t] = solver.BoolVar('y_' + str(t))

# Objective
obj = 0
for t in T:
    obj += c * P[t] + F * y[t] + h * I[t]
solver.Minimize(obj)

# Constraints
# 1. Inventory Balance
for t in T:
    if t == 1:
        solver.Add(I[t] == P[t] - d[t])
    else:
        solver.Add(I[t] == I[t - 1] + P[t] - d[t])

# 2. End-of-Horizon Inventory Constraint
solver.Add(I[6] == 0)

# 3. Production Capacity (already enforced by variable bounds, but explicit for clarity)
for t in T:
    solver.Add(P[t] <= U)

# 4. Warehouse Storage Capacity (already enforced by variable bounds)
for t in T:
    solver.Add(I[t] <= W)

# 5. Fixed Cost Linking
for t in T:
    solver.Add(P[t] <= U * y[t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")