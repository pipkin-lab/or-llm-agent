from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Define plan sets for each factory
P = dict()
P[1] = [1, 2, 3]
P[2] = [1, 2, 3, 4]
P[3] = [1, 2]

# Define cost and return parameters
C = dict()
C[1, 1] = 0
C[1, 2] = 1
C[1, 3] = 2
C[2, 1] = 0
C[2, 2] = 2
C[2, 3] = 3
C[2, 4] = 4
C[3, 1] = 0
C[3, 2] = 1

R = dict()
R[1, 1] = 0
R[1, 2] = 5
R[1, 3] = 6
R[2, 1] = 0
R[2, 2] = 8
R[2, 3] = 9
R[2, 4] = 12
R[3, 1] = 0
R[3, 2] = 3

B = 5

# Create binary decision variables
x = dict()
for i in [1, 2, 3]:
    for j in P[i]:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Constraint 1: Exactly one plan per factory
for i in [1, 2, 3]:
    solver.Add(sum(x[i, j] for j in P[i]) == 1)

# Constraint 2: Budget constraint
total_cost = sum(C[i, j] * x[i, j] for i in [1, 2, 3] for j in P[i])
solver.Add(total_cost <= B)

# Objective: Maximize total return
total_return = sum(R[i, j] * x[i, j] for i in [1, 2, 3] for j in P[i])
solver.Maximize(total_return)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")