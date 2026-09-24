from ortools.linear_solver import pywraplp

# Model parameters
c = dict()
c[1] = 28
c[2] = 45
c[3] = 60
c[4] = 73

requirements = dict()
requirements[1] = 1500
requirements[2] = 1000
requirements[3] = 2000
requirements[4] = 1200

# Valid index pairs for x[i, j] where i + j - 1 <= 4
valid_pairs = list()
for i in range(1, 5):
    for j in range(1, 5):
        if i + j - 1 <= 4:
            valid_pairs.append((i, j))

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Create decision variables
x = dict()
for i in range(1, 5):
    for j in range(1, 5):
        if i + j - 1 <= 4:
            x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

# Objective function
obj = 0
for i in range(1, 5):
    for j in range(1, 5):
        if i + j - 1 <= 4:
            obj += c[j] * x[i, j]
solver.Minimize(obj)

# Capacity constraints for each month t
for t in range(1, 5):
    expr = 0
    for i in range(1, 5):
        for j in range(1, 5):
            if i + j - 1 <= 4:
                # Contract (i, j) is active in month t if i <= t and i + j - 1 >= t
                if i <= t and i + j - 1 >= t:
                    expr += x[i, j]
    solver.Add(expr >= requirements[t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")