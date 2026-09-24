from ortools.linear_solver import pywraplp

# Define the problem
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index set I = {1, 2, 3, 4, 5, 6}
I = [1, 2, 3, 4, 5, 6]
n = len(I)

# Parameters
Cap = dict()
Dem = dict()
c = dict()
F = dict()

Cap[1] = 1500
Cap[2] = 2500
Cap[3] = 4000
Cap[4] = 6000
Cap[5] = 9000
Cap[6] = 12000

Dem[1] = 500
Dem[2] = 550
Dem[3] = 700
Dem[4] = 900
Dem[5] = 400
Dem[6] = 300

c[1] = 5
c[2] = 8
c[3] = 10
c[4] = 12
c[5] = 16
c[6] = 18

F[1] = 1200
F[2] = 1200
F[3] = 1200
F[4] = 1200
F[5] = 1200
F[6] = 1200

# M_i: upper bound on total production of type i
M = dict()
for i in I:
    M[i] = 0
    for j in I:
        if Cap[j] <= Cap[i]:
            M[i] += Dem[j]

# Decision variables
# x[i, j]: quantity of container type i produced to satisfy demand for container type j
# Only defined for i >= j (since D_ij = {j, j+1, ..., 6})
x = dict()
for i in I:
    for j in I:
        if i >= j:
            x[i, j] = solver.NumVar(0, solver.infinity(), 'x_{}_{}'.format(i, j))
        else:
            x[i, j] = solver.NumVar(0, 0, 'x_{}_{}'.format(i, j))

# y[i]: binary variable indicating if machine i is turned on
y = dict()
for i in I:
    y[i] = solver.BoolVar('y_{}'.format(i))

# Objective function: Minimize total cost
obj = 0
for i in I:
    obj += F[i] * y[i]
    for j in I:
        if i >= j:
            obj += c[i] * x[i, j]

solver.Minimize(obj)

# Demand satisfaction constraints
for j in I:
    demand_expr = 0
    for i in I:
        if i >= j:
            demand_expr += x[i, j]
    solver.Add(demand_expr == Dem[j])

# Machine activation linking constraints (Big-M)
for i in I:
    prod_expr = 0
    for j in I:
        if i >= j:
            prod_expr += x[i, j]
    solver.Add(prod_expr <= M[i] * y[i])

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")