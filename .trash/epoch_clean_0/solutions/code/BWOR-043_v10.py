from ortools.linear_solver import pywraplp

# Define solver
solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Parameters
I = [0, 1, 2, 3]  # Origins 1-4 (0-indexed)
J = [0, 1, 2, 3, 4, 5]  # Destinations 1-6 (0-indexed)

S = [50, 40, 60, 31]
D = [30, 50, 20, 40, 30, 11]

c = [
    [2, 1, 3, 3, 3, 5],
    [4, 2, 2, 4, 4, 4],
    [3, 5, 4, 2, 4, 1],
    [4, 2, 2, 1, 2, 2]
]

# Decision variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, inf, 'x_' + str(i) + '_' + str(j))

# Objective function
obj = 0
for i in I:
    for j in J:
        obj += c[i][j] * x[i, j]
solver.Minimize(obj)

# Supply constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) == S[i])

# Demand constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")