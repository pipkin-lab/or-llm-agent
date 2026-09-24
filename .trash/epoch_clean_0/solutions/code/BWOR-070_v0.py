from ortools.linear_solver import pywraplp

# Initialize the solver (MILP since variables are integers)
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    print("No solver available")
    exit(1)

# Parameters
w = [0, 2, 3, 4, 5]  # w[1..4]
v = [0, 2, 2, 2, 3]  # v[1..4]
c = [0, 3, 4, 5, 6]  # c[1..4]
W_max = 15
V_max = 10

# Decision variables: x_i for i in 1..4, non-negative integers
x = dict()
for i in range(1, 5):
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

# Objective function: Maximize total value
obj_terms = []
for i in range(1, 5):
    obj_terms.append(c[i] * x[i])
solver.Maximize(sum(obj_terms))

# Constraint 1: Weight capacity
weight_expr = 0
for i in range(1, 5):
    weight_expr += w[i] * x[i]
solver.Add(weight_expr <= W_max)

# Constraint 2: Volume capacity
volume_expr = 0
for i in range(1, 5):
    volume_expr += v[i] * x[i]
solver.Add(volume_expr <= V_max)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")