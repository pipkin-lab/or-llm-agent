from ortools.linear_solver import pywraplp

# Parameters
products = [1, 2, 3]
w = dict()
w[1] = 2
w[2] = 3
w[3] = 4

p = dict()
p[1] = 100
p[2] = 140
p[3] = 180

W = 10

# MILP Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x_i for i in {1, 2, 3}, non-negative integers
x = dict()
for i in products:
    x[i] = solver.IntVar(0, INF, 'x_' + str(i))

# Objective: maximize total profit
obj = 0
for i in products:
    obj += p[i] * x[i]

solver.Maximize(obj)

# Constraint: total weight <= capacity
weight_expr = 0
for i in products:
    weight_expr += w[i] * x[i]

solver.Add(weight_expr <= W)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")