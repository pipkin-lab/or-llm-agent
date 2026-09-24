from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
P = [1, 2, 3]

# Parameters
a1 = dict()
a1[1] = 3
a1[2] = 2
a1[3] = 6

a2 = dict()
a2[1] = 4
a2[2] = 3
a2[3] = 6

pi = dict()
pi[1] = 60
pi[2] = 40
pi[3] = 100

F = dict()
F[1] = 2000
F[2] = 1500
F[3] = 1000

L_avail = 150
M_avail = 160

U = dict()
U[1] = 40
U[2] = 53
U[3] = 25

# Decision Variables
x = dict()
y = dict()
for i in P:
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))
    y[i] = solver.BoolVar('y_' + str(i))

# Objective Function
obj = 0
for i in P:
    obj += pi[i] * x[i] - F[i] * y[i]

solver.Maximize(obj)

# Resource Constraints
labor_constraint = 0
for i in P:
    labor_constraint += a1[i] * x[i]
solver.Add(labor_constraint <= L_avail)

material_constraint = 0
for i in P:
    material_constraint += a2[i] * x[i]
solver.Add(material_constraint <= M_avail)

# Linking Constraints (Big-M)
for i in P:
    solver.Add(x[i] <= U[i] * y[i])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")