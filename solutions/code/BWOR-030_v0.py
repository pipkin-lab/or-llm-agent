from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
C_max = 5000
S_0 = 1000
K_0 = 20000
I_target = 2000

months = [1, 2, 3]
Pb = dict()
Ps = dict()
Pb[1] = 2.85
Pb[2] = 3.05
Pb[3] = 2.90
Ps[1] = 3.10
Ps[2] = 3.25
Ps[3] = 2.95

# Decision variables
x = dict()
y = dict()
I = dict()
B = dict()
for t in months:
    x[t] = solver.NumVar(0, INF, 'x_' + str(t))
    y[t] = solver.NumVar(0, INF, 'y_' + str(t))
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))
    B[t] = solver.NumVar(0, INF, 'B_' + str(t))

# Inventory balance constraints
solver.Add(I[1] == S_0 + x[1] - y[1])
solver.Add(I[2] == I[1] + x[2] - y[2])
solver.Add(I[3] == I[2] + x[3] - y[3])

# Sales availability constraints
solver.Add(y[1] <= S_0)
solver.Add(y[2] <= I[1])
solver.Add(y[3] <= I[2])

# Capacity constraints
for t in months:
    solver.Add(I[t] <= C_max)

# Cash flow balance constraints
solver.Add(B[1] == K_0 + Ps[1] * y[1] - Pb[1] * x[1])
solver.Add(B[2] == B[1] + Ps[2] * y[2] - Pb[2] * x[2])
solver.Add(B[3] == B[2] + Ps[3] * y[3] - Pb[3] * x[3])

# Ending inventory constraint
solver.Add(I[3] == I_target)

# Objective: maximize B_3
solver.Maximize(B[3])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")