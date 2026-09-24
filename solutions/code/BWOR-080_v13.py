from ortools.linear_solver import pywraplp

# Parameters
T = list(range(1, 7))  # Months 1 to 6
P = list(range(1, 8))  # Products 1 to 7
M = list(range(1, 6))  # Machine types 1 to 5

# Machine hours per unit of product (a[m][p])
a = dict()
a[1] = dict()  # Grinding
a[1][1] = 0.5; a[1][2] = 0.7; a[1][3] = 0.0; a[1][4] = 0.0; a[1][5] = 0.3; a[1][6] = 0.2; a[1][7] = 0.5
a[2] = dict()  # Upright Drill
a[2][1] = 0.1; a[2][2] = 0.2; a[2][3] = 0.0; a[2][4] = 0.3; a[2][5] = 0.0; a[2][6] = 0.6; a[2][7] = 0.0
a[3] = dict()  # Horizontal Drill
a[3][1] = 0.2; a[3][2] = 0.0; a[3][3] = 0.8; a[3][4] = 0.0; a[3][5] = 0.0; a[3][6] = 0.0; a[3][7] = 0.6
a[4] = dict()  # Boring Machine
a[4][1] = 0.05; a[4][2] = 0.03; a[4][3] = 0.0; a[4][4] = 0.07; a[4][5] = 0.1; a[4][6] = 0.0; a[4][7] = 0.08
a[5] = dict()  # Planer
a[5][1] = 0.0; a[5][2] = 0.0; a[5][3] = 0.01; a[5][4] = 0.0; a[5][5] = 0.05; a[5][6] = 0.0; a[5][7] = 0.05

# Profit per unit
c = dict()
c[1] = 100; c[2] = 60; c[3] = 80; c[4] = 40; c[5] = 110; c[6] = 90; c[7] = 30

# Demand D[t][p]
D = dict()
D[1] = dict(); D[1][1]=500; D[1][2]=1000; D[1][3]=300; D[1][4]=300; D[1][5]=800; D[1][6]=200; D[1][7]=100
D[2] = dict(); D[2][1]=600; D[2][2]=500; D[2][3]=200; D[2][4]=0; D[2][5]=400; D[2][6]=300; D[2][7]=150
D[3] = dict(); D[3][1]=300; D[3][2]=600; D[3][3]=0; D[3][4]=0; D[3][5]=500; D[3][6]=400; D[3][7]=100
D[4] = dict(); D[4][1]=200; D[4][2]=300; D[4][3]=400; D[4][4]=500; D[4][5]=200; D[4][6]=0; D[4][7]=100
D[5] = dict(); D[5][1]=0; D[5][2]=100; D[5][3]=500; D[5][4]=100; D[5][5]=1000; D[5][6]=300; D[5][7]=0
D[6] = dict(); D[6][1]=500; D[6][2]=500; D[6][3]=100; D[6][4]=300; D[6][5]=1100; D[6][6]=500; D[6][7]=60

# Available hours H[t][m]
H = dict()
H[1] = dict(); H[1][1]=1152; H[1][2]=768; H[1][3]=1152; H[1][4]=384; H[1][5]=384
H[2] = dict(); H[2][1]=1536; H[2][2]=768; H[2][3]=384; H[2][4]=384; H[2][5]=384
H[3] = dict(); H[3][1]=1536; H[3][2]=768; H[3][3]=1152; H[3][4]=0; H[3][5]=384
H[4] = dict(); H[4][1]=1536; H[4][2]=384; H[4][3]=1152; H[4][4]=384; H[4][5]=384
H[5] = dict(); H[5][1]=1152; H[5][2]=384; H[5][3]=1152; H[5][4]=384; H[5][5]=384
H[6] = dict(); H[6][1]=1536; H[6][2]=768; H[6][3]=768; H[6][4]=384; H[6][5]=0

# Storage cost per unit per month
h_storage = 5
# Max inventory
S_max = 100
# Final inventory required
I_final = 50

# Create LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()   # x[t, p]
s = dict()   # s[t, p]
I = dict()   # I[t, p]

for t in T:
    for p in P:
        x[t, p] = solver.NumVar(0, INF, 'x_%d_%d' % (t, p))
        s[t, p] = solver.NumVar(0, INF, 's_%d_%d' % (t, p))
        I[t, p] = solver.NumVar(0, S_max, 'I_%d_%d' % (t, p))

# Objective: Maximize sum(c_p * s[t,p]) - sum(5 * I[t,p])
obj = 0
for t in T:
    for p in P:
        obj += c[p] * s[t, p]
        obj -= h_storage * I[t, p]
solver.Maximize(obj)

# Demand constraints: s[t, p] <= D[t, p]
for t in T:
    for p in P:
        solver.Add(s[t, p] <= D[t][p])

# Inventory balance: I[t, p] = I[t-1, p] + x[t, p] - s[t, p]
for t in T:
    for p in P:
        if t == 1:
            solver.Add(I[t, p] == 0 + x[t, p] - s[t, p])
        else:
            solver.Add(I[t, p] == I[t - 1, p] + x[t, p] - s[t, p])

# Final inventory requirement: I[6, p] = 50
for p in P:
    solver.Add(I[6, p] == I_final)

# Machine capacity constraints
for t in T:
    for m in M:
        expr = 0
        for p in P:
            expr += a[m][p] * x[t, p]
        solver.Add(expr <= H[t][m])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")