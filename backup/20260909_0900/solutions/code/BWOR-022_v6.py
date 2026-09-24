import math
from ortools.linear_solver import pywraplp

# Data
C = [0, 1, 2]  # components 1, 2, 3 (0-indexed)
K = [0, 1, 2]  # spare parts levels 1, 2, 3 (0-indexed)

reliability = {
    (0, 0): 0.3, (0, 1): 0.4, (0, 2): 0.5,
    (1, 0): 0.2, (1, 1): 0.5, (1, 2): 0.9,
    (2, 0): 0.1, (2, 1): 0.2, (2, 2): 0.7
}

cost = {
    (0, 0): 1, (0, 1): 2, (0, 2): 3,
    (1, 0): 3, (1, 1): 5, (1, 2): 6,
    (2, 0): 2, (2, 1): 3, (2, 2): 4
}

B = 8

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Variables
x = dict()
for c in C:
    for k in K:
        x[c, k] = solver.BoolVar('x_' + str(c) + '_' + str(k))

# Constraints
# Allocation: exactly one k per component
for c in C:
    solver.Add(sum(x[c, k] for k in K) == 1)

# Budget constraint
solver.Add(sum(cost[c, k] * x[c, k] for c in C for k in K) <= B)

# Objective: maximize sum of ln(reliability)
obj = 0
for c in C:
    for k in K:
        obj += math.log(reliability[c, k]) * x[c, k]

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # Compute the actual system reliability (product of reliabilities)
    total_reliability = 1.0
    for c in C:
        for k in K:
            if x[c, k].solution_value() > 0.5:
                total_reliability *= reliability[c, k]
    print("OPTIMAL_VALUE:", total_reliability)
else:
    print("NO_FEASIBLE_SOLUTION")