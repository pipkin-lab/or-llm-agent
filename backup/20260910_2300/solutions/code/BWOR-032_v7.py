from ortools.linear_solver import pywraplp

# Sets
T = range(1, 13)  # Months 1 to 12
P = [1, 2]        # Products 1 and 2

# Parameters
# Demand
D = dict()
for t in T:
    if t in range(1, 5):
        D[(1, t)] = 10000
    elif t in range(5, 10):
        D[(1, t)] = 30000
    else:  # t in 10, 11, 12
        D[(1, t)] = 100000

    if t in [1, 2, 10, 11, 12]:
        D[(2, t)] = 50000
    else:  # t in 3..9
        D[(2, t)] = 15000

# Production cost
C = dict()
for t in T:
    if t in range(1, 6):
        C[(1, t)] = 5.0
        C[(2, t)] = 8.0
    else:  # t in 6..12
        C[(1, t)] = 4.5
        C[(2, t)] = 7.0

# Volume per unit
V = dict()
V[1] = 0.2
V[2] = 0.4

# Capacities
Cap_prod = 120000
Cap_wh = 15000

# Holding costs
H_in = 1.0
H_out = 1.5

# Solver initialization (LP)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
x = dict()      # x[p, t]: production of product p in month t
I = dict()      # I[p, t]: inventory of product p at end of month t
S_in = dict()   # S_in[t]: volume in in-house warehouse at end of month t
S_out = dict()  # S_out[t]: volume in external warehouse at end of month t

for p in P:
    for t in T:
        x[p, t] = solver.NumVar(0, solver.infinity(), 'x_{}_{}'.format(p, t))
        I[p, t] = solver.NumVar(0, solver.infinity(), 'I_{}_{}'.format(p, t))

for t in range(1, 12):
    S_in[t] = solver.NumVar(0, solver.infinity(), 'S_in_{}'.format(t))
    S_out[t] = solver.NumVar(0, solver.infinity(), 'S_out_{}'.format(t))

# Objective function
obj = 0
for t in T:
    for p in P:
        obj += C[p, t] * x[p, t]

for t in range(1, 12):
    obj += H_in * S_in[t] + H_out * S_out[t]

solver.Minimize(obj)

# Constraints

# 1. Inventory balance
# I[p, t] = I[p, t-1] + x[p, t] - D[p, t]
for p in P:
    for t in T:
        if t == 1:
            # I[p, 0] = 0
            solver.Add(I[p, t] == x[p, t] - D[p, t])
        else:
            solver.Add(I[p, t] == I[p, t - 1] + x[p, t] - D[p, t])

# 2. Ending inventory = 0
for p in P:
    solver.Add(I[p, 12] == 0)

# 3. Production capacity
for t in T:
    solver.Add(x[1, t] + x[2, t] <= Cap_prod)

# 4. Storage volume balance
for t in range(1, 12):
    solver.Add(S_in[t] + S_out[t] == V[1] * I[1, t] + V[2] * I[2, t])

# 5. In-house capacity
for t in range(1, 12):
    solver.Add(S_in[t] <= Cap_wh)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")