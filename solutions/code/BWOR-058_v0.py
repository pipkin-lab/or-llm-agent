from ortools.linear_solver import pywraplp

# Parameters
I = [1, 2, 3, 4, 5]
K = [1, 2, 3]

# Area per store for category i
a = dict()
a[1] = 250
a[2] = 350
a[3] = 800
a[4] = 400
a[5] = 500

# Min and Max number of stores for category i
L = dict()
L[1] = 1
L[2] = 1
L[3] = 1
L[4] = 0
L[5] = 1

U = dict()
U[1] = 3
U[2] = 2
U[3] = 3
U[4] = 2
U[5] = 3

# Rental income coefficients c[i][k] = 0.2 * Profit[i][k]
c = dict()
c[1, 1] = 1.8
c[1, 2] = 1.6
c[1, 3] = 1.4
c[2, 1] = 2.0
c[2, 2] = 1.8
c[3, 1] = 5.4
c[3, 2] = 4.2
c[3, 3] = 4.0
c[4, 1] = 3.2
c[4, 2] = 2.0
c[5, 1] = 3.4
c[5, 2] = 3.0
c[5, 3] = 2.4

# Total available area
A_total = 5000

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x[i, k] binary, only for k in [L[i], U[i]]
x = dict()
for i in I:
    for k in range(L[i], U[i] + 1):
        x[i, k] = solver.IntVar(0, 1, 'x_' + str(i) + '_' + str(k))

# Objective: Maximize total rental income
obj_terms = []
for i in I:
    for k in range(L[i], U[i] + 1):
        obj_terms.append(c[i, k] * x[i, k])
objective = sum(obj_terms)
solver.Maximize(objective)

# Constraint 1: Exclusivity - exactly one k per category i
for i in I:
    solver.Add(sum(x[i, k] for k in range(L[i], U[i] + 1)) == 1)

# Constraint 2: Area constraint
area_terms = []
for i in I:
    for k in range(L[i], U[i] + 1):
        area_terms.append(a[i] * k * x[i, k])
solver.Add(sum(area_terms) <= A_total)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")