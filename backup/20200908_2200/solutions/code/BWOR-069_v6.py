from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index set
J = [1, 2, 3]

# Parameters
w = {1: 2, 2: 3, 3: 4}
p = {1: 100, 2: 140, 3: 180}
W_max = 10

# Decision variables: non-negative integers
x = {}
for j in J:
    x[j] = solver.IntVar(0, solver.infinity(), 'x_' + str(j))

# Objective function: maximize total profit
objective = 0
for j in J:
    objective += p[j] * x[j]

solver.Maximize(objective)

# Constraint: total weight <= W_max
weight_constraint = 0
for j in J:
    weight_constraint += w[j] * x[j]
solver.Add(weight_constraint <= W_max)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")