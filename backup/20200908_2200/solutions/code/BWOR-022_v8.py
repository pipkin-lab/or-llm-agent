import math
from ortools.linear_solver import pywraplp

# Define solver (MILP since variables are binary)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
K = [1, 2, 3]  # Components
J = [1, 2, 3]  # Number of spare parts

# Parameters
B = 8  # Total budget limit (thousand yuan)

# Reliability R[k][j]
R = dict()
R[1] = [0.0, 0.3, 0.4, 0.5]
R[2] = [0.0, 0.2, 0.5, 0.9]
R[3] = [0.0, 0.1, 0.2, 0.7]

# Cost C[k][j]
C = dict()
C[1] = [0, 1, 2, 3]
C[2] = [0, 3, 5, 6]
C[3] = [0, 2, 3, 4]

# V[k][j] = ln(R[k][j])
V = dict()
for k in K:
    V[k] = [0.0]
    for j in J:
        V[k].append(math.log(R[k][j]))

# Decision variables x[k][j] binary
x = dict()
for k in K:
    x[k] = dict()
    for j in J:
        x[k][j] = solver.BoolVar('x_' + str(k) + '_' + str(j))

# Objective: Maximize sum V[k][j] * x[k][j]
obj = 0
for k in K:
    for j in J:
        obj += V[k][j] * x[k][j]
solver.Maximize(obj)

# Constraint 1: For each component k, exactly one j is selected
for k in K:
    solver.Add(sum(x[k][j] for j in J) == 1)

# Constraint 2: Budget limit
total_cost = 0
for k in K:
    for j in J:
        total_cost += C[k][j] * x[k][j]
solver.Add(total_cost <= B)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")