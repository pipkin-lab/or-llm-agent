from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
I = [1, 2, 3]
Z = [1, 2, 3]

# Parameters
r = dict()
r[1, 1] = 0.3
r[1, 2] = 0.4
r[1, 3] = 0.5
r[2, 1] = 0.2
r[2, 2] = 0.5
r[2, 3] = 0.9
r[3, 1] = 0.1
r[3, 2] = 0.2
r[3, 3] = 0.7

c = dict()
c[1, 1] = 1
c[1, 2] = 2
c[1, 3] = 3
c[2, 1] = 3
c[2, 2] = 5
c[2, 3] = 6
c[3, 1] = 2
c[3, 2] = 3
c[3, 3] = 4

B = 8

# Decision variables
x = dict()
for i in I:
    for z in Z:
        x[i, z] = solver.BoolVar('x_' + str(i) + '_' + str(z))

# Objective: maximize total reliability gain
obj = 0
for i in I:
    for z in Z:
        obj += r[i, z] * x[i, z]

solver.Maximize(obj)

# Constraints
# 1. Selection constraint: exactly one level per part type
for i in I:
    solver.Add(sum(x[i, z] for z in Z) == 1)

# 2. Budget constraint
total_cost = 0
for i in I:
    for z in Z:
        total_cost += c[i, z] * x[i, z]
solver.Add(total_cost <= B)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")