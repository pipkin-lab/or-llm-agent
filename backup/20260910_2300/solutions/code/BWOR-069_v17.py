from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x_i for i in {1, 2, 3}, non-negative integers
x = dict()
for i in range(1, 4):
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

# Parameters
w = dict()
w[1] = 2
w[2] = 3
w[3] = 4

p = dict()
p[1] = 100
p[2] = 140
p[3] = 180

W_max = 10

# Objective: Maximize total profit
objective = 0
for i in range(1, 4):
    objective += p[i] * x[i]
solver.Maximize(objective)

# Constraint: Total weight <= W_max
weight_expr = 0
for i in range(1, 4):
    weight_expr += w[i] * x[i]
solver.Add(weight_expr <= W_max)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")