import math
from ortools.linear_solver import pywraplp

# Parameters
I = [1, 2, 3]
K = [1, 2, 3]

# Reliability matrix r[i][k] (0-indexed internally)
R = [
    [0.3, 0.4, 0.5],  # Component 1
    [0.2, 0.5, 0.9],  # Component 2
    [0.1, 0.2, 0.7]   # Component 3
]

# Cost matrix c[i][k]
C = [
    [1, 2, 3],  # Component 1
    [3, 5, 6],  # Component 2
    [2, 3, 4]   # Component 3
]

# Budget
B = 8

# Pre-calculate log of reliabilities
LogR = [[math.log(R[i][k]) for k in range(3)] for i in range(3)]

# Create solver (MILP because of binary variables)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables y[i][k]
y = dict()
for i in range(3):
    for k in range(3):
        y[i, k] = solver.BoolVar('y_' + str(i + 1) + '_' + str(k + 1))

# Constraints
# 1. Selection constraint: exactly one option per component
for i in range(3):
    solver.Add(sum(y[i, k] for k in range(3)) == 1)

# 2. Budget constraint
solver.Add(sum(C[i][k] * y[i, k] for i in range(3) for k in range(3)) <= B)

# Objective: Maximize sum of LogR[i][k] * y[i][k]
obj = sum(LogR[i][k] * y[i, k] for i in range(3) for k in range(3))
solver.Maximize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # Reconstruct the original reliability R = exp(Z) = product of selected reliabilities
    # Find the selected option for each component
    selected_reliability = 1.0
    for i in range(3):
        for k in range(3):
            if y[i, k].solution_value() > 0.5:
                selected_reliability *= R[i][k]
    print("OPTIMAL_VALUE:", selected_reliability)
else:
    print("NO_FEASIBLE_SOLUTION")