from ortools.linear_solver import pywraplp

# Parameters
months = [1, 2, 3, 4, 5, 6]
quantities = [10, 20, 30, 40, 50]

D = dict()
D[1] = 40
D[2] = 20
D[3] = 30
D[4] = 40
D[5] = 30
D[6] = 20

Cq = dict()
Cq[10] = 48
Cq[20] = 86
Cq[30] = 118
Cq[40] = 138
Cq[50] = 160

h = 0.2
F = 10
I_max = 40

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Variables
y = dict()
for t in months:
    for q in quantities:
        y[t, q] = solver.BoolVar('y_' + str(t) + '_' + str(q))

I = dict()
for t in months:
    I[t] = solver.NumVar(0, INF, 'I_' + str(t))

# Objective
obj_terms = []
for t in months:
    for q in quantities:
        obj_terms.append((Cq[q] + F) * y[t, q])
for t in months:
    obj_terms.append(h * I[t])

solver.Minimize(sum(obj_terms))

# Constraints

# 1. At most one order per month
for t in months:
    expr = sum(y[t, q] for q in quantities)
    solver.Add(expr <= 1)

# 2. Inventory balance
for t in months:
    order_qty = sum(q * y[t, q] for q in quantities)
    if t == 1:
        solver.Add(I[t] == order_qty - D[t])
    else:
        solver.Add(I[t] == I[t - 1] + order_qty - D[t])

# 3. End-of-season inventory = 0
solver.Add(I[6] == 0)

# 4. Inventory capacity
for t in months:
    solver.Add(I[t] <= I_max)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")