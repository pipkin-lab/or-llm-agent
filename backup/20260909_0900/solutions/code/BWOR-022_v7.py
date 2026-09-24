from ortools.linear_solver import pywraplp
import math

# Define the solver (MILP since variables are binary)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
J = [0, 1, 2]  # Components 1, 2, 3 (0-indexed)
K = [0, 1, 2]  # Spare part options 1, 2, 3 (0-indexed)

# Parameters: Cost C[j][k]
C = [
    [1, 2, 3],  # Component 1 (j=0)
    [3, 5, 6],  # Component 2 (j=1)
    [2, 3, 4]   # Component 3 (j=2)
]

# Parameters: Reliability R[j][k]
R = [
    [0.3, 0.4, 0.5],  # Component 1
    [0.2, 0.5, 0.9],  # Component 2
    [0.1, 0.2, 0.7]   # Component 3
]

# Parameters: Log Reliability L[j][k]
L = [
    [math.log(0.3), math.log(0.4), math.log(0.5)],
    [math.log(0.2), math.log(0.5), math.log(0.9)],
    [math.log(0.1), math.log(0.2), math.log(0.7)]
]

# Budget limit
B = 8

# Decision Variables: x[j][k] is 1 if component j is allocated k+1 spare parts
x = dict()
for j in J:
    for k in K:
        x[j, k] = solver.BoolVar('x_' + str(j) + '_' + str(k))

# Allocation Completeness Constraint: Each component gets exactly one option
for j in J:
    solver.Add(sum(x[j, k] for k in K) == 1)

# Budget Constraint
total_cost = sum(C[j][k] * x[j, k] for j in J for k in K)
solver.Add(total_cost <= B)

# Objective: Maximize sum of log reliabilities
objective = sum(L[j][k] * x[j, k] for j in J for k in K)
solver.Maximize(objective)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # Reconstruct the actual product of reliabilities
    total_reliability = 1.0
    for j in J:
        for k in K:
            if x[j, k].solution_value() > 0.5:
                total_reliability *= R[j][k]
    print("OPTIMAL_VALUE:", total_reliability)
else:
    print("NO_FEASIBLE_SOLUTION")