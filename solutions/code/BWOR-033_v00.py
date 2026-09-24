from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

products = [1, 2, 3]
quarters = [1, 2, 3, 4]

# Decision variables
x = dict()
I = dict()
L = dict()

for i in products:
    for t in quarters:
        x[i, t] = solver.NumVar(0, INF, 'x_%d_%d' % (i, t))
        I[i, t] = solver.NumVar(0, INF, 'I_%d_%d' % (i, t))
        L[i, t] = solver.NumVar(0, INF, 'L_%d_%d' % (i, t))

# Parameter data
C_L = {1: 20, 2: 20, 3: 10}
C_I = {1: 5, 2: 5, 3: 5}

D = dict()
D[(1, 1)] = 1500
D[(1, 2)] = 1000
D[(1, 3)] = 2000
D[(1, 4)] = 1200
D[(2, 1)] = 1500
D[(2, 2)] = 1500
D[(2, 3)] = 1200
D[(2, 4)] = 1500
D[(3, 1)] = 1000
D[(3, 2)] = 2000
D[(3, 3)] = 1500
D[(3, 4)] = 2500

# Objective
obj_expr = 0
for i in products:
    for t in quarters:
        obj_expr += C_L[i] * L[i, t] + C_I[i] * I[i, t]
solver.Minimize(obj_expr)

# Inventory balance constraints
for i in products:
    for t in quarters:
        if t == 1:
            solver.Add(I[i, t] - L[i, t] == x[i, t] - D[(i, t)])
        else:
            solver.Add(I[i, t] - L[i, t] == I[i, t-1] - L[i, t-1] + x[i, t] - D[(i, t)])

# Final inventory requirement
for i in products:
    solver.Add(I[i, 4] - L[i, 4] == 150)
    solver.Add(L[i, 4] == 0)

# Production capacity constraints
hours_per_unit = {1: 2, 2: 4, 3: 3}
for t in quarters:
    solver.Add(hours_per_unit[1] * x[1, t] + hours_per_unit[2] * x[2, t] + hours_per_unit[3] * x[3, t] <= 15000)

# Product-specific production restriction
solver.Add(x[1, 2] == 0)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")