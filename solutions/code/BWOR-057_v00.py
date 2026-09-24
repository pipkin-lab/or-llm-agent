from ortools.linear_solver import pywraplp

# Data
I = [1, 2, 3, 4, 5, 6]
N = [1, 2, 3, 4, 5, 6]
capacity = {1: 1500, 2: 2500, 3: 4000, 4: 6000, 5: 9000, 6: 12000}
D = {1: 500, 2: 550, 3: 700, 4: 900, 5: 400, 6: 300}
c = {1: 5, 2: 8, 3: 10, 4: 12, 5: 16, 6: 18}
F = {i: 1200 for i in I}
D_total = sum(D[j] for j in N)

# Solver (MILP because y_i are binary and x_ij should be integer)
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Variables
x = dict()
for i in I:
    for j in N:
        if capacity[i] >= capacity[j]:
            x[i, j] = solver.IntVar(0, INF, 'x_%d_%d' % (i, j))

y = dict()
for i in I:
    y[i] = solver.BoolVar('y_%d' % i)

# Objective
obj = 0
for i in I:
    obj += F[i] * y[i]
for i in I:
    for j in N:
        if capacity[i] >= capacity[j]:
            obj += c[i] * x[i, j]
solver.Minimize(obj)

# Demand satisfaction constraints
for j in N:
    expr = 0
    for i in I:
        if capacity[i] >= capacity[j]:
            expr += x[i, j]
    solver.Add(expr == D[j])

# Machine activation linking constraints
for i in I:
    expr = 0
    for j in N:
        if capacity[i] >= capacity[j]:
            expr += x[i, j]
    solver.Add(expr <= D_total * y[i])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")