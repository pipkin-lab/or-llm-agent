from ortools.linear_solver import pywraplp

# Index sets
M = [1, 2, 3, 4]
D = [1, 2, 3, 4]

# Parameters
R = dict()
R[1] = 1500
R[2] = 1000
R[3] = 2000
R[4] = 1200

c = dict()
c[1] = 28
c[2] = 45
c[3] = 60
c[4] = 73

# Valid (m, d) pairs where m + d - 1 <= 4
valid_pairs = []
for m in M:
    for d in D:
        if m + d - 1 <= 4:
            valid_pairs.append((m, d))

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
x = dict()
for (m, d) in valid_pairs:
    x[(m, d)] = solver.NumVar(0, solver.infinity(), 'x_' + str(m) + '_' + str(d))

# Objective function
obj = 0
for (m, d) in valid_pairs:
    obj += c[d] * x[(m, d)]
solver.Minimize(obj)

# Demand satisfaction constraints
for t in M:
    constraint_expr = 0
    for (m, d) in valid_pairs:
        if m <= t <= m + d - 1:
            constraint_expr += x[(m, d)]
    solver.Add(constraint_expr >= R[t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")