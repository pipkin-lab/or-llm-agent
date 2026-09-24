from ortools.linear_solver import pywraplp

# Model Type: LP (Continuous variables for production planning)
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index Sets
T = list(range(1, 13))  # Months 1 to 12
P = [1, 2]              # Products 1 and 2

# Parameters
# Demand D[p][t]
D = dict()
for p in P:
    D[p] = dict()
    for t in T:
        if p == 1:
            if t <= 4:
                D[p][t] = 10000
            elif t <= 9:
                D[p][t] = 30000
            else:
                D[p][t] = 100000
        else:  # p == 2
            if t in [1, 2, 10, 11, 12]:
                D[p][t] = 50000
            else:
                D[p][t] = 15000

# Production Costs c[p][t]
c = dict()
for p in P:
    c[p] = dict()
    for t in T:
        if p == 1:
            if t <= 5:
                c[p][t] = 5.0
            else:
                c[p][t] = 4.5
        else:  # p == 2
            if t <= 5:
                c[p][t] = 8.0
            else:
                c[p][t] = 7.0

# Capacity and Volume
Capacity = 120000
v = dict()
v[1] = 0.2
v[2] = 0.4
W_cap = 15000
h_in = 1.0
h_ext = 1.5

# Decision Variables
# x[p][t]: Production of product p in month t
x = dict()
for p in P:
    x[p] = dict()
    for t in T:
        x[p][t] = solver.NumVar(0, INF, 'x_' + str(p) + '_' + str(t))

# I[p][t]: Inventory of product p at end of month t
I = dict()
for p in P:
    I[p] = dict()
    for t in T:
        I[p][t] = solver.NumVar(0, INF, 'I_' + str(p) + '_' + str(t))

# V_in[t]: Internal volume used at end of month t
V_in = dict()
for t in T:
    V_in[t] = solver.NumVar(0, INF, 'V_in_' + str(t))

# S[t]: External volume rented at end of month t
S = dict()
for t in T:
    S[t] = solver.NumVar(0, INF, 'S_' + str(t))

# Constraints

# 1. Inventory Balance: I[p][t-1] + x[p][t] = D[p][t] + I[p][t]
for p in P:
    for t in T:
        if t == 1:
            solver.Add(x[p][1] == D[p][1] + I[p][1])
        else:
            solver.Add(I[p][t - 1] + x[p][t] == D[p][t] + I[p][t])

# 2. Production Capacity: x[1][t] + x[2][t] <= Capacity
for t in T:
    solver.Add(x[1][t] + x[2][t] <= Capacity)

# 3. Volume Balance: V_in[t] + S[t] = v[1]*I[1][t] + v[2]*I[2][t]
for t in T:
    solver.Add(V_in[t] + S[t] == v[1] * I[1][t] + v[2] * I[2][t])

# 4. Internal Warehouse Limit: V_in[t] <= W_cap
for t in T:
    solver.Add(V_in[t] <= W_cap)

# Objective Function
# Min Z = sum(c[p][t] * x[p][t]) + sum(h_in * V_in[t] + h_ext * S[t])
obj_terms = []
for p in P:
    for t in T:
        obj_terms.append(c[p][t] * x[p][t])

for t in T:
    obj_terms.append(h_in * V_in[t])
    obj_terms.append(h_ext * S[t])

solver.Minimize(sum(obj_terms))

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")