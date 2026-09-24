from ortools.linear_solver import pywraplp

# Parameters
P = dict()
P[1] = 410
P[2] = 430
P[3] = 460
P[4] = 450

S = dict()
S[1] = 425
S[2] = 440
S[3] = 465
S[4] = 455

D = dict()
D[1] = 100
D[2] = 140
D[3] = 200
D[4] = 160

K = 20
a = 70
b = 100

quarters = [1, 2, 3, 4]

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
for t in quarters:
    x[t] = solver.NumVar(0, INF, 'x_' + str(t))

y = dict()
for t in quarters:
    for s in range(t, 5):
        y[t, s] = solver.NumVar(0, INF, 'y_' + str(t) + '_' + str(s))

I = dict()
for t in quarters:
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))

# Objective function
obj = 0
for t in quarters:
    for s in range(t, 5):
        profit = S[s] - P[t] - (a / 1000.0 + b / 1000.0 * (s - t))
        obj += profit * y[t, s]

solver.Maximize(obj)

# Constraint 1: Flow Conservation
for t in quarters:
    expr = sum(y[t, s] for s in range(t, 5)) + I[t]
    solver.Add(x[t] == expr)

# Constraint 2: Inventory Balance
for t in quarters:
    sales_in_t = sum(y[tau, t] for tau in range(1, t + 1))
    if t == 1:
        solver.Add(I[1] == x[1] - sales_in_t)
    else:
        solver.Add(I[t] == I[t - 1] + x[t] - sales_in_t)

# Constraint 3: Warehouse Capacity
for t in quarters:
    solver.Add(I[t] <= K)

# Constraint 4: Sales Volume Limits
for s in quarters:
    solver.Add(sum(y[t, s] for t in range(1, s + 1)) <= D[s])

# Constraint 5: End-of-Year Clearance
solver.Add(I[4] == 0)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")