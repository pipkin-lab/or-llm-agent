from ortools.linear_solver import pywraplp

# Parameters
C = [1500, 2500, 4000, 6000, 9000, 12000]
D = [500, 550, 700, 900, 400, 300]
v = [5, 8, 10, 12, 16, 18]
F = 1200

n = len(C)

# Define substitution sets S_i: j in S_i if C_j >= C_i
# Also compute U_j: sum of D_i for i where C_i <= C_j
U = [0] * n
for j in range(n):
    for i in range(n):
        if C[j] >= C[i]:
            U[j] += D[i]

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
inf = solver.infinity()

# Decision variables
x = dict()
for i in range(n):
    for j in range(n):
        if C[j] >= C[i]:
            x[i, j] = solver.NumVar(0, inf, 'x_{}_{}'.format(i, j))

y = dict()
for j in range(n):
    y[j] = solver.BoolVar('y_{}'.format(j))

# Objective function
obj = 0
for i in range(n):
    for j in range(n):
        if C[j] >= C[i]:
            obj += v[j] * x[i, j]
for j in range(n):
    obj += F * y[j]

solver.Minimize(obj)

# Demand satisfaction constraints
for i in range(n):
    demand_expr = 0
    for j in range(n):
        if C[j] >= C[i]:
            demand_expr += x[i, j]
    solver.Add(demand_expr == D[i])

# Fixed charge linkage constraints (Big-M)
for j in range(n):
    prod_expr = 0
    for i in range(n):
        if C[j] >= C[i]:
            prod_expr += x[i, j]
    solver.Add(prod_expr <= U[j] * y[j])

# Solve
status = solver.Solve()
if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")