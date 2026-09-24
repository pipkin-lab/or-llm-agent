from ortools.linear_solver import pywraplp

# Index sets
V = [1, 2, 3, 4]
N = len(V)

# Distance matrix (1-indexed)
d = dict()
d[1, 2] = 6
d[1, 3] = 7
d[1, 4] = 9
d[2, 1] = 8
d[2, 3] = 9
d[2, 4] = 7
d[3, 1] = 5
d[3, 2] = 8
d[3, 4] = 8
d[4, 1] = 6
d[4, 2] = 5
d[4, 3] = 5
for i in V:
    d[i, i] = 0

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x[i, j] binary for i != j
x = dict()
for i in V:
    for j in V:
        if i != j:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))

# MTZ auxiliary variables: u[i] for i in {2, 3, 4}
u = dict()
u[1] = solver.NumVar(0, 0, 'u_1')
for i in [2, 3, 4]:
    u[i] = solver.IntVar(0, N - 1, 'u_{}'.format(i))

# Objective: minimize total distance
obj = 0
for i in V:
    for j in V:
        if i != j:
            obj += d[i, j] * x[i, j]
solver.Minimize(obj)

# Flow conservation constraints
for i in V:
    # In-degree = 1
    in_expr = sum(x[j, i] for j in V if j != i)
    solver.Add(in_expr == 1)
    # Out-degree = 1
    out_expr = sum(x[i, j] for j in V if j != i)
    solver.Add(out_expr == 1)

# MTZ subtour elimination constraints
for i in [2, 3, 4]:
    for j in [2, 3, 4]:
        if i != j:
            solver.Add(u[i] - u[j] + N * x[i, j] <= N - 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")