from ortools.linear_solver import pywraplp

# Model Type: MILP
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index Sets
V = [1, 2, 3, 4]
N = len(V)

# Distance matrix d[i][j]
d = dict()
# d[i][j] = distance from i to j
d[1, 1] = 0
d[1, 2] = 6
d[1, 3] = 7
d[1, 4] = 9
d[2, 1] = 8
d[2, 2] = 0
d[2, 3] = 9
d[2, 4] = 7
d[3, 1] = 5
d[3, 2] = 8
d[3, 3] = 0
d[3, 4] = 8
d[4, 1] = 6
d[4, 2] = 5
d[4, 3] = 5
d[4, 4] = 0

# Decision Variables
# x[i, j] = 1 if the path travels from i to j, else 0
x = dict()
for i in V:
    for j in V:
        if i != j:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))

# u[i]: continuous auxiliary variable for MTZ subtour elimination
u = dict()
for i in V:
    if i == 1:
        u[i] = solver.NumVar(0, 0, 'u_{}'.format(i))
    else:
        u[i] = solver.NumVar(0, N - 1, 'u_{}'.format(i))

# Objective: minimize total distance
obj = 0
for i in V:
    for j in V:
        if i != j:
            obj += d[i, j] * x[i, j]
solver.Minimize(obj)

# Constraint 1: Flow Conservation (Out-degree)
# Every city must have exactly one outgoing arc
for i in V:
    out_expr = 0
    for j in V:
        if i != j:
            out_expr += x[i, j]
    solver.Add(out_expr == 1)

# Constraint 2: Flow Conservation (In-degree)
# Every city must have exactly one incoming arc
for j in V:
    in_expr = 0
    for i in V:
        if i != j:
            in_expr += x[i, j]
    solver.Add(in_expr == 1)

# Constraint 3: Subtour Elimination (Miller-Tucker-Zemlin)
# u_i - u_j + N * x_ij <= N - 1 for all i, j in V \ {1}, i != j
for i in V:
    if i == 1:
        continue
    for j in V:
        if j == 1 or i == j:
            continue
        solver.Add(u[i] - u[j] + N * x[i, j] <= N - 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")