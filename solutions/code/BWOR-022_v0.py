import math
from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
I = [1, 2, 3]
K = [1, 2, 3]

# Parameters
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

L = dict()
for i in I:
    for k in K:
        L[i, k] = math.log(R[i, k])

B = 8

# Decision variables: x[i, k] binary
x = dict()
for i in I:
    for k in K:
        x[i, k] = solver.BoolVar('x_' + str(i) + '_' + str(k))

# Objective: Maximize sum of L[i,k] * x[i,k]
obj_terms = []
for i in I:
    for k in K:
        obj_terms.append(L[i, k] * x[i, k])
solver.Maximize(sum(obj_terms))

# Selection constraints: for each component, exactly one k is chosen
for i in I:
    solver.Add(sum(x[i, k] for k in K) == 1)

# Budget constraint
cost_terms = []
for i in I:
    for k in K:
        cost_terms.append(C[i, k] * x[i, k])
solver.Add(sum(cost_terms) <= B)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")