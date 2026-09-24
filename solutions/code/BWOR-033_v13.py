from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

products = ['I', 'II', 'III']
quarters = [1, 2, 3, 4]

# Parameters
D = dict()
D[('I', 1)] = 1500; D[('I', 2)] = 1000; D[('I', 3)] = 2000; D[('I', 4)] = 1200
D[('II', 1)] = 1500; D[('II', 2)] = 1500; D[('II', 3)] = 1200; D[('II', 4)] = 1500
D[('III', 1)] = 1000; D[('III', 2)] = 2000; D[('III', 3)] = 1500; D[('III', 4)] = 2500

H = dict()
for t in quarters:
    H[t] = 15000

h = dict()
h['I'] = 2; h['II'] = 4; h['III'] = 3

cL = dict()
cL['I'] = 20; cL['II'] = 20; cL['III'] = 10

cI = dict()
cI['I'] = 5; cI['II'] = 5; cI['III'] = 5

E = dict()
E['I'] = 150; E['II'] = 150; E['III'] = 150

I0 = dict()
for i in products:
    I0[i] = 0

# Decision variables
x = dict()
for i in products:
    for t in quarters:
        x[i, t] = solver.NumVar(0, INF, 'x_' + i + '_' + str(t))

I = dict()
for i in products:
    for t in quarters:
        I[i, t] = solver.NumVar(0, INF, 'I_' + i + '_' + str(t))

L = dict()
for i in products:
    for t in quarters:
        L[i, t] = solver.NumVar(0, INF, 'L_' + i + '_' + str(t))

# Constraint 3: Production restriction - Product I cannot be produced in Q2
solver.Add(x['I', 2] == 0)

# Constraint 1: Inventory Balance
for i in products:
    for t in quarters:
        if t == 1:
            solver.Add(x[i, 1] + I0[i] + L[i, 1] - I[i, 1] == D[i, 1])
        else:
            solver.Add(x[i, t] + I[i, t - 1] + L[i, t] - I[i, t] == D[i, t])

# Constraint 2: Production Capacity
for t in quarters:
    expr = 0
    for i in products:
        expr += h[i] * x[i, t]
    solver.Add(expr <= H[t])

# Constraint 4: Ending Inventory
for i in products:
    solver.Add(I[i, 4] == E[i])

# Objective Function: Minimize Z
obj = 0
for i in products:
    for t in quarters:
        obj += cL[i] * L[i, t] + cI[i] * I[i, t]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")