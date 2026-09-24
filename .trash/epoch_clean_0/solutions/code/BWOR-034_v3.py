from ortools.linear_solver import pywraplp

# Problem parameters
R = {1: 1500, 2: 1000, 3: 2000, 4: 1200}
C = {1: 28, 2: 45, 3: 60, 4: 73}

# Valid (t, d) pairs
valid_pairs = []
for t in range(1, 5):
    for d in range(1, 5):
        if t + d - 1 <= 4:
            valid_pairs.append((t, d))

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Create variables
x = dict()
for (t, d) in valid_pairs:
    x[t, d] = solver.NumVar(0, solver.infinity(), 'x_' + str(t) + '_' + str(d))

# Objective function
obj = 0
for (t, d) in valid_pairs:
    obj += C[d] * x[t, d]

solver.Minimize(obj)

# Constraints for each month t: sum of x[i, d] where i <= t <= i+d-1 >= R[t]
for t in range(1, 5):
    constraint_expr = 0
    for (i, d) in valid_pairs:
        if i <= t <= i + d - 1:
            constraint_expr += x[i, d]
    solver.Add(constraint_expr >= R[t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")