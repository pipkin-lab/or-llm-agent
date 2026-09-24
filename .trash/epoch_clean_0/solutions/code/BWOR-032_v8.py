from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
months = list(range(1, 13))
products = ['I', 'II']

# Demand
d = dict()
for t in months:
    if t <= 4:
        d[('I', t)] = 10000
    elif t <= 9:
        d[('I', t)] = 30000
    else:
        d[('I', t)] = 100000

    if t in [1, 2, 10, 11, 12]:
        d[('II', t)] = 50000
    else:
        d[('II', t)] = 15000

# Production Costs
c = dict()
for t in months:
    if t <= 5:
        c[('I', t)] = 5.00
        c[('II', t)] = 8.00
    else:
        c[('I', t)] = 4.50
        c[('II', t)] = 7.00

# Volumes
V = dict()
V['I'] = 0.2
V['II'] = 0.4

# Capacities
C_prod = 120000
W_cap = 15000

# Storage Costs
h_in = 1.00
h_out = 1.50

# Decision Variables
x = dict()
u = dict()
e = dict()

for p in products:
    for t in months:
        x[p, t] = solver.NumVar(0, solver.infinity(), 'x_{}_{}'.format(p, t))
        u[p, t] = solver.NumVar(0, solver.infinity(), 'u_{}_{}'.format(p, t))
        e[p, t] = solver.NumVar(0, solver.infinity(), 'e_{}_{}'.format(p, t))

# Objective Function
obj = 0
for t in months:
    for p in products:
        obj += c[p, t] * x[p, t]
    obj += h_in * (V['I'] * u['I', t] + V['II'] * u['II', t])
    obj += h_out * (V['I'] * e['I', t] + V['II'] * e['II', t])

solver.Minimize(obj)

# Constraints

# 1. Inventory Balance
for t in months:
    for p in products:
        if t == 1:
            solver.Add(u[p, t] + e[p, t] == x[p, t] - d[p, t])
        else:
            solver.Add(u[p, t] + e[p, t] == u[p, t-1] + e[p, t-1] + x[p, t] - d[p, t])

# 2. In-House Warehouse Capacity
for t in months:
    solver.Add(V['I'] * u['I', t] + V['II'] * u['II', t] <= W_cap)

# 3. Production Capacity
for t in months:
    solver.Add(x['I', t] + x['II', t] <= C_prod)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")