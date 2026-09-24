from ortools.linear_solver import pywraplp

# Problem parameters
months = list(range(1, 13))  # t = 1 to 12
products = [1, 2]  # i = 1, 2

# Volume per unit (m^3)
v = dict()
v[1] = 0.2
v[2] = 0.4

# Holding costs (yuan/m^3/month)
h_in = 1.0
h_out = 1.5

# Production cost per unit
c_prod = dict()
for t in months:
    if t <= 5:
        c_prod[1, t] = 5.00
        c_prod[2, t] = 8.00
    else:
        c_prod[1, t] = 4.50
        c_prod[2, t] = 7.00

# Demand (units)
d = dict()
for t in months:
    # Product I
    if t <= 4:
        d[1, t] = 10000
    elif t <= 9:
        d[1, t] = 30000
    else:
        d[1, t] = 100000
    # Product II
    if t in [1, 2, 10, 11, 12]:
        d[2, t] = 50000
    else:
        d[2, t] = 15000

# Monthly production capacity (units)
monthly_capacity = 120000

# In-house warehouse capacity (m^3)
warehouse_capacity = 15000

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
s = dict()
r = dict()

for i in products:
    for t in months:
        x[i, t] = solver.NumVar(0, INF, 'x_{}_{}'.format(i, t))
        s[i, t] = solver.NumVar(0, INF, 's_{}_{}'.format(i, t))
        r[i, t] = solver.NumVar(0, INF, 'r_{}_{}'.format(i, t))

# Objective function: Minimize total cost
obj_terms = []
for t in months:
    for i in products:
        obj_terms.append(c_prod[i, t] * x[i, t])
    # In-house holding cost
    obj_terms.append(h_in * sum(v[i] * s[i, t] for i in products))
    # External holding cost
    obj_terms.append(h_out * sum(v[i] * r[i, t] for i in products))

solver.Minimize(sum(obj_terms))

# Constraints

# A. Inventory balance: s[i,t] + r[i,t] = s[i,t-1] + r[i,t-1] + x[i,t] - d[i,t]
for t in months:
    for i in products:
        if t == 1:
            # s[i,0] = 0, r[i,0] = 0
            solver.Add(s[i, t] + r[i, t] == x[i, t] - d[i, t])
        else:
            solver.Add(s[i, t] + r[i, t] == s[i, t - 1] + r[i, t - 1] + x[i, t] - d[i, t])

# B. Production capacity: x[1,t] + x[2,t] <= 120,000
for t in months:
    solver.Add(x[1, t] + x[2, t] <= monthly_capacity)

# C. Warehouse volume constraint: sum_i v_i * s[i,t] <= 15,000
for t in months:
    solver.Add(sum(v[i] * s[i, t] for i in products) <= warehouse_capacity)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")