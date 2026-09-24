from ortools.linear_solver import pywraplp

# Data
# Good types: 1, 2, 3, 4
I = [1, 2, 3, 4]

# Weights (tons)
w = {1: 2, 2: 3, 3: 4, 4: 5}

# Volumes (m^3)
v = {1: 2, 2: 2, 3: 2, 4: 3}

# Values (thousand yuan)
c = {1: 3, 2: 4, 3: 5, 4: 6}

# Capacities
W_max = 15
V_max = 10

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x_i for i in I, non-negative integers
# Upper bounds can be derived from capacities
# x_i <= min(W_max // w[i], V_max // v[i])
x = dict()
for i in I:
    upper_bound = min(W_max // w[i], V_max // v[i])
    x[i] = solver.IntVar(0, upper_bound, 'x_' + str(i))

# Constraints
# Weight constraint: sum(w_i * x_i) <= W_max
weight_expr = sum(w[i] * x[i] for i in I)
solver.Add(weight_expr <= W_max)

# Volume constraint: sum(v_i * x_i) <= V_max
volume_expr = sum(v[i] * x[i] for i in I)
solver.Add(volume_expr <= V_max)

# Objective function: Maximize total value
obj_expr = sum(c[i] * x[i] for i in I)
solver.Maximize(obj_expr)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")