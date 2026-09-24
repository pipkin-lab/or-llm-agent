from ortools.linear_solver import pywraplp

# Initialize solver (Continuous LP)
solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Index sets
T = range(1, 13)
I = range(1, 3)

# Parameters
# Demand D[i][t]
D = dict()
for i in I:
    for t in T:
        if i == 1:
            if t in [1, 2, 3, 4]:
                D[i, t] = 10000
            elif t in [5, 6, 7, 8, 9]:
                D[i, t] = 30000
            else: # 10, 11, 12
                D[i, t] = 100000
        else: # i == 2
            if t in [3, 4, 5, 6, 7, 8, 9]:
                D[i, t] = 15000
            else: # 1, 2, 10, 11, 12
                D[i, t] = 50000

# Production Cost c[i][t]
c = dict()
for i in I:
    for t in T:
        if i == 1:
            if t <= 5:
                c[i, t] = 5.0
            else:
                c[i, t] = 4.5
        else: # i == 2
            if t <= 5:
                c[i, t] = 8.0
            else:
                c[i, t] = 7.0

# Capacity
C_t = 120000

# Storage Parameters
v = {1: 0.2, 2: 0.4}
V_wh = 15000
h_in = 1.0
h_out = 1.5

# Unit storage costs (yuan/unit/month)
h_unit_in = {1: h_in * v[1], 2: h_in * v[2]}
h_unit_out = {1: h_out * v[1], 2: h_out * v[2]}

# Decision Variables
# x[i, t]: Production of product i in month t
x = dict()
for i in I:
    for t in T:
        x[i, t] = solver.NumVar(0, inf, 'x_' + str(i) + '_' + str(t))

# I[i, t]: Internal inventory of product i at end of month t
I_var = dict()
for i in I:
    for t in T:
        I_var[i, t] = solver.NumVar(0, inf, 'I_' + str(i) + '_' + str(t))

# E[i, t]: External inventory of product i at end of month t
E = dict()
for i in I:
    for t in T:
        E[i, t] = solver.NumVar(0, inf, 'E_' + str(i) + '_' + str(t))

# Constraints

# A. Inventory Balance Constraints
# I[i, t] + E[i, t] = I[i, t-1] + E[i, t-1] + x[i, t] - D[i, t]
# For t=1, I[i,0]=0, E[i,0]=0
for i in I:
    for t in T:
        if t == 1:
            prev_I = 0
            prev_E = 0
        else:
            prev_I = I_var[i, t - 1]
            prev_E = E[i, t - 1]
        
        # I[i, t] + E[i, t] - x[i, t] = prev_I + prev_E - D[i, t]
        # Rearranged for solver.Add:
        # I[i, t] + E[i, t] - x[i, t] == prev_I + prev_E - D[i, t]
        # Since prev_I and prev_E are variables (except t=1), we move them to LHS or RHS appropriately.
        # pywraplp.Add accepts linear expressions.
        # LHS: I[i, t] + E[i, t] - x[i, t]
        # RHS: prev_I + prev_E - D[i, t]
        # If t>1, prev_I and prev_E are variables.
        # Expression: I[i, t] + E[i, t] - x[i, t] - prev_I - prev_E == -D[i, t]
        
        if t == 1:
            solver.Add(I_var[i, 1] + E[i, 1] - x[i, 1] == -D[i, 1])
        else:
            solver.Add(I_var[i, t] + E[i, t] - x[i, t] - I_var[i, t - 1] - E[i, t - 1] == -D[i, t])

# B. In-House Warehouse Capacity Constraint
# 0.2 * I[1, t] + 0.4 * I[2, t] <= 15000
for t in T:
    solver.Add(v[1] * I_var[1, t] + v[2] * I_var[2, t] <= V_wh)

# C. Production Capacity Constraint
# x[1, t] + x[2, t] <= 120000
for t in T:
    solver.Add(x[1, t] + x[2, t] <= C_t)

# Objective Function
# Minimize Z = sum(c[i, t] * x[i, t] + h_unit_in[i] * I[i, t] + h_unit_out[i] * E[i, t])
obj_terms = []
for t in T:
    for i in I:
        obj_terms.append(c[i, t] * x[i, t])
        obj_terms.append(h_unit_in[i] * I_var[i, t])
        obj_terms.append(h_unit_out[i] * E[i, t])

solver.Minimize(sum(obj_terms))

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")