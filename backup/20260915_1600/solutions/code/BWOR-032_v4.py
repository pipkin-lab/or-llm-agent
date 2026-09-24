from ortools.linear_solver import pywraplp

# Model Type: LP (Continuous variables) - using GLOP
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index Sets
T = list(range(1, 13))  # Months 1..12
P = [1, 2]              # Products 1, 2

# Parameters
# Demand D[p][t]
D = dict()
D[1] = dict()
D[2] = dict()
for t in T:
    if t in [1, 2, 3, 4]:
        D[1][t] = 10000
    elif t in [5, 6, 7, 8, 9]:
        D[1][t] = 30000
    elif t in [10, 11, 12]:
        D[1][t] = 100000

    if t in [3, 4, 5, 6, 7, 8, 9]:
        D[2][t] = 15000
    else:  # 1, 2, 10, 11, 12
        D[2][t] = 50000

# Production Cost C[p][t]
C = dict()
C[1] = dict()
C[2] = dict()
for t in T:
    if t <= 5:
        C[1][t] = 5.0
        C[2][t] = 8.0
    else:
        C[1][t] = 4.5
        C[2][t] = 7.0

# Volume per unit
v = dict()
v[1] = 0.2
v[2] = 0.4

# Storage Costs
h_in = 1.0
h_ext = 1.5

# Capacities
W_in = 15000.0
Cap_prod = 120000

# Decision Variables
# x[p][t]: production
x = dict()
for p in P:
    for t in T:
        x[p, t] = solver.NumVar(0, INF, 'x_' + str(p) + '_' + str(t))

# I[p][t]: total inventory in units at end of month t
I = dict()
for p in P:
    for t in T:
        I[p, t] = solver.NumVar(0, INF, 'I_' + str(p) + '_' + str(t))

# V_in[p][t]: internal storage volume (m3)
V_in = dict()
for p in P:
    for t in T:
        V_in[p, t] = solver.NumVar(0, INF, 'Vin_' + str(p) + '_' + str(t))

# V_ext[p][t]: external storage volume (m3)
V_ext = dict()
for p in P:
    for t in T:
        V_ext[p, t] = solver.NumVar(0, INF, 'Vext_' + str(p) + '_' + str(t))

# Objective Function
obj = 0
for t in T:
    for p in P:
        obj += C[p][t] * x[p, t]
        obj += h_in * V_in[p, t]
        obj += h_ext * V_ext[p, t]

solver.Minimize(obj)

# Constraints

# A. Inventory Balance
for p in P:
    for t in T:
        if t == 1:
            # I[p][0] = 0
            solver.Add(I[p, t] == 0 + x[p, t] - D[p][t])
        else:
            solver.Add(I[p, t] == I[p, t - 1] + x[p, t] - D[p][t])

# B. Volume Conservation
for p in P:
    for t in T:
        solver.Add(V_in[p, t] + V_ext[p, t] == I[p, t] * v[p])

# C. Internal Warehouse Capacity
for t in T:
    total_vol_in = 0
    for p in P:
        total_vol_in += V_in[p, t]
    solver.Add(total_vol_in <= W_in)

# D. Monthly Production Capacity
for t in T:
    total_prod = 0
    for p in P:
        total_prod += x[p, t]
    solver.Add(total_prod <= Cap_prod)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")