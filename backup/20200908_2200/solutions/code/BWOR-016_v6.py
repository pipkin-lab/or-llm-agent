from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
I = range(4)  # Factories 1-4 (0-indexed: 0-3)
J = range(4)  # Demand locations 1-4 (0-indexed: 0-3)
K = [2, 3]    # Potential new factories (0-indexed: 2, 3 corresponding to A3, A4)

# Parameters
u = [400, 600, 200, 200]  # Capacities
d = [350, 400, 300, 150]  # Demands

# Cost matrix c[i][j]
c = [
    [2, 9, 3, 4],
    [8, 3, 5, 7],
    [7, 6, 1, 2],
    [4, 5, 2, 5]
]

# Fixed costs for building new factories
F = {2: 1200, 3: 1500}

# Decision Variables
# x[i][j] >= 0: amount transported from factory i to location j
x = {}
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

# y[k] in {0, 1}: whether factory k is built (k in {2, 3} for 0-indexed A3, A4)
y = {}
for k in K:
    y[k] = solver.IntVar(0, 1, 'y_' + str(k))

# Objective Function: Minimize total cost
obj = 0
for k in K:
    obj += F[k] * y[k]
for i in I:
    for j in J:
        obj += c[i][j] * x[i, j]

solver.Minimize(obj)

# Constraints

# A. Capacity Constraints
# For factory 0 (A1): sum_j x[0][j] <= 400
solver.Add(sum(x[0, j] for j in J) <= u[0])

# For factory 1 (A2): sum_j x[1][j] <= 600
solver.Add(sum(x[1, j] for j in J) <= u[1])

# For factory 2 (A3): sum_j x[2][j] <= 200 * y[2]
solver.Add(sum(x[2, j] for j in J) <= u[2] * y[2])

# For factory 3 (A4): sum_j x[3][j] <= 200 * y[3]
solver.Add(sum(x[3, j] for j in J) <= u[3] * y[3])

# B. Demand Satisfaction Constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) == d[j])

# C. Construction Logic: Build exactly one new factory
solver.Add(y[2] + y[3] == 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")