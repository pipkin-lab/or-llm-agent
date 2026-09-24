import math
from ortools.linear_solver import pywraplp

# Parameters from Table 7-19
# x is the number of spare parts, indexed 1 to 3
# Components: 1, 2, 3

# Reliability R_i(x)
R = dict()
R[1, 1] = 0.3
R[1, 2] = 0.4
R[1, 3] = 0.5
R[2, 1] = 0.2
R[2, 2] = 0.5
R[2, 3] = 0.9
R[3, 1] = 0.1
R[3, 2] = 0.2
R[3, 3] = 0.7

# Cost C_i(x) in thousand yuan
C = dict()
C[1, 1] = 1
C[1, 2] = 2
C[1, 3] = 3
C[2, 1] = 3
C[2, 2] = 5
C[2, 3] = 6
C[3, 1] = 2
C[3, 2] = 3
C[3, 3] = 4

# Budget constraint
BUDGET = 8

# Decision variables: x[i] is the number of spares for component i (i in {1, 2, 3})
# Since x[i] is in {1, 2, 3}, we use binary variables y[i, x] indicating if component i gets x spares
# y[i, x] = 1 if component i gets x spares, 0 otherwise, for x in {1, 2, 3}

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Create binary variables y[i, x]
y = dict()
for i in [1, 2, 3]:
    for x in [1, 2, 3]:
        y[i, x] = solver.BoolVar('y_' + str(i) + '_' + str(x))

# Constraint: Each component must get exactly one allocation
for i in [1, 2, 3]:
    solver.Add(sum(y[i, x] for x in [1, 2, 3]) == 1)

# Budget constraint: Sum of costs <= BUDGET
# Cost = sum over i and x of C[i, x] * y[i, x]
cost_expr = 0
for i in [1, 2, 3]:
    for x in [1, 2, 3]:
        cost_expr += C[i, x] * y[i, x]
solver.Add(cost_expr <= BUDGET)

# Objective: Maximize sum of ln(R_i(x_i))
# ln(R_i(x_i)) = sum over x of ln(R_i(x)) * y[i, x]
# Since we are maximizing a constant times a binary, and ln is monotonic, this is linear in y.
obj = 0
for i in [1, 2, 3]:
    for x in [1, 2, 3]:
        obj += math.log(R[i, x]) * y[i, x]

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")