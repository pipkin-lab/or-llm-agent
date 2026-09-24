from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

P = [1, 2, 3]

a_steel = dict()
a_steel[1] = 1.5
a_steel[2] = 3.0
a_steel[3] = 5.0

a_labor = dict()
a_labor[1] = 300
a_labor[2] = 250
a_labor[3] = 400

c = dict()
c[1] = 2000
c[2] = 3000
c[3] = 4000

S_steel = 6000
S_labor = 600000
B = 1000

M = dict()
M[1] = 2000
M[2] = 2000
M[3] = 1200

x = dict()
y = dict()
for p in P:
    x[p] = solver.NumVar(0, INF, 'x_' + str(p))
    y[p] = solver.BoolVar('y_' + str(p))

# Objective
obj = 0
for p in P:
    obj += c[p] * x[p]
solver.Maximize(obj)

# Resource constraints
solver.Add(1.5 * x[1] + 3.0 * x[2] + 5.0 * x[3] <= S_steel)
solver.Add(300 * x[1] + 250 * x[2] + 400 * x[3] <= S_labor)

# Semi-continuous linking constraints
for p in P:
    solver.Add(x[p] <= M[p] * y[p])
    solver.Add(x[p] >= B * y[p])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")