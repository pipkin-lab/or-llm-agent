from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Data: R_i(x) and C_i(x) for i in {1, 2, 3}, x in {0, 1, 2, 3}
# Using dictionaries keyed by (component, x_value)
R = dict()
C = dict()

# Component 1
R[(1, 0)] = 0.0; C[(1, 0)] = 0
R[(1, 1)] = 0.3; C[(1, 1)] = 1
R[(1, 2)] = 0.4; C[(1, 2)] = 2
R[(1, 3)] = 0.5; C[(1, 3)] = 3

# Component 2
R[(2, 0)] = 0.0; C[(2, 0)] = 0
R[(2, 1)] = 0.2; C[(2, 1)] = 3
R[(2, 2)] = 0.5; C[(2, 2)] = 5
R[(2, 3)] = 0.9; C[(2, 3)] = 6

# Component 3
R[(3, 0)] = 0.0; C[(3, 0)] = 0
R[(3, 1)] = 0.1; C[(3, 1)] = 2
R[(3, 2)] = 0.2; C[(3, 2)] = 3
R[(3, 3)] = 0.7; C[(3, 3)] = 4

# Decision variables: x_i for i in {1, 2, 3}, x_i in {0, 1, 2, 3}
# We'll use integer variables
x = dict()
for i in range(1, 4):
    x[i] = solver.IntVar(0, 3, 'x_' + str(i))

# Objective: Maximize total reliability increase
# Z = R_1(x_1) + R_2(x_2) + R_3(x_3)
# Since R_i(x_i) is a non-linear (piecewise) function of x_i, we need to linearize.
# We can use auxiliary variables or expand the objective using indicator-like formulation.
# Alternatively, since x_i is bounded and small, we can use a standard MILP formulation
# with additional binary variables or simply enumerate... but let's use a proper MILP.
#
# Actually, for small discrete domains, we can use the following approach:
# Introduce y[i][v] binary variable = 1 if x_i = v
# Then x_i = sum_v v * y[i][v]
# R_i(x_i) = sum_v R[(i,v)] * y[i][v]
# C_i(x_i) = sum_v C[(i,v)] * y[i][v]

y = dict()
for i in range(1, 4):
    for v in range(0, 4):
        y[(i, v)] = solver.BoolVar('y_' + str(i) + '_' + str(v))

# Constraint: x_i = sum_v v * y[i][v]
for i in range(1, 4):
    solver.Add(x[i] == sum(v * y[(i, v)] for v in range(0, 4)))

# Constraint: sum_v y[i][v] = 1 for each i
for i in range(1, 4):
    solver.Add(sum(y[(i, v)] for v in range(0, 4)) == 1)

# Objective: Maximize sum_i sum_v R[(i,v)] * y[(i,v)]
obj = sum(R[(i, v)] * y[(i, v)] for i in range(1, 4) for v in range(0, 4))
solver.Maximize(obj)

# Budget constraint: sum_i C_i(x_i) <= 8
# C_i(x_i) = sum_v C[(i,v)] * y[(i,v)]
budget_expr = sum(C[(i, v)] * y[(i, v)] for i in range(1, 4) for v in range(0, 4))
solver.Add(budget_expr <= 8)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")