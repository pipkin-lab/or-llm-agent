from ortools.linear_solver import pywraplp

# Parameters
P = [1, 2, 3]
Z = [0, 1, 2, 3]
B = 8

# Reliability increase r[p][z]
r = dict()
r[1] = dict(); r[1][0] = 0.0; r[1][1] = 0.3; r[1][2] = 0.4; r[1][3] = 0.5
r[2] = dict(); r[2][0] = 0.0; r[2][1] = 0.2; r[2][2] = 0.5; r[2][3] = 0.9
r[3] = dict(); r[3][0] = 0.0; r[3][1] = 0.1; r[3][2] = 0.2; r[3][3] = 0.7

# Cost c[p][z]
c = dict()
c[1] = dict(); c[1][0] = 0; c[1][1] = 1; c[1][2] = 2; c[1][3] = 3
c[2] = dict(); c[2][0] = 0; c[2][1] = 3; c[2][2] = 5; c[2][3] = 6
c[3] = dict(); c[3][0] = 0; c[3][1] = 2; c[3][2] = 3; c[3][3] = 4

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[p][z]
x = dict()
for p in P:
    for z in Z:
        x[p, z] = solver.BoolVar('x_' + str(p) + '_' + str(z))

# Constraint 1: Exactly one level per part type
for p in P:
    solver.Add(sum(x[p, z] for z in Z) == 1)

# Constraint 2: Budget
solver.Add(sum(c[p][z] * x[p, z] for p in P for z in Z) <= B)

# Objective: Maximize total reliability
obj = sum(r[p][z] * x[p, z] for p in P for z in Z)
solver.Maximize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")