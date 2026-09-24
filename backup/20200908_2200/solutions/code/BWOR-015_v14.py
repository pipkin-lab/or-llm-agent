from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    print("NO_SOLVER_AVAILABLE")
    exit()

INF = solver.infinity()

# Indices
I = range(3)  # Products 1, 2, 3 (0-indexed)
T = range(3)  # Stages 1, 2, 3 (0-indexed)

# Parameters
D = dict()
D[0, 0] = 500; D[1, 0] = 750; D[2, 0] = 900
D[0, 1] = 680; D[1, 1] = 800; D[2, 1] = 800
D[0, 2] = 800; D[1, 2] = 950; D[2, 2] = 1000

a = [2.0, 1.0, 3.1]
b = [40, 20, 55]
H = 5000
C = 93000
w = [1, 1, 2]

# Variables
x = dict()
Inv = dict()
u = dict()
ep = dict()
em = dict()
cp = dict()
cm = dict()

for i in I:
    for t in T:
        x[i, t] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(t))
        Inv[i, t] = solver.NumVar(0, INF, 'Inv_' + str(i) + '_' + str(t))
        u[i, t] = solver.NumVar(0, INF, 'u_' + str(i) + '_' + str(t))

for t in T:
    ep[t] = solver.NumVar(0, INF, 'ep_' + str(t))
    em[t] = solver.NumVar(0, INF, 'em_' + str(t))
    cp[t] = solver.NumVar(0, INF, 'cp_' + str(t))
    cm[t] = solver.NumVar(0, INF, 'cm_' + str(t))

# Constraints
# 1. Inventory Balance: x[i,t] + Inv[i,t-1] - Inv[i,t] + u[i,t] = D[i,t]
for i in I:
    for t in T:
        if t == 0:
            beg_inv = 0
        else:
            beg_inv = Inv[i, t - 1]
        
        if t == 2:
            # Final inventory must be 0
            solver.Add(x[i, t] + beg_inv + u[i, t] == D[i, t])
        else:
            solver.Add(x[i, t] + beg_inv - Inv[i, t] + u[i, t] == D[i, t])

# 2. Equipment Hours: sum(a[i]*x[i,t]) + em[t] - ep[t] = H
for t in T:
    expr = sum(a[i] * x[i, t] for i in I)
    solver.Add(expr + em[t] - ep[t] == H)

# 3. Working Capital: sum(b[i]*x[i,t]) + cm[t] - cp[t] = C
for t in T:
    expr = sum(b[i] * x[i, t] for i in I)
    solver.Add(expr + cm[t] - cp[t] == C)

# Objective: Lexicographic Minimization via Large Weights
# Weights: P1 = 1000000, P2 = 1000, P3 = 1
W1 = 1000000
W2 = 1000
W3 = 1

obj = 0
# Z1: Minimize weighted stockouts
for i in I:
    for t in T:
        obj += W1 * w[i] * u[i, t]

# Z2: Minimize equipment overloading
for t in T:
    obj += W2 * ep[t]

# Z3: Minimize capital overloading
for t in T:
    obj += W3 * cp[t]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")