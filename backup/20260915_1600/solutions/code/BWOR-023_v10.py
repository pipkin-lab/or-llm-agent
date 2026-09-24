from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Cities: 1, 2, 3, 4
cities = [1, 2, 3, 4]
N = 4

# Distance matrix (symmetric)
d = dict()
d[1, 2] = 6
d[1, 3] = 7
d[1, 4] = 9
d[2, 3] = 9
d[2, 4] = 7
d[3, 4] = 8
d[2, 1] = 6
d[3, 1] = 7
d[4, 1] = 9
d[3, 2] = 9
d[4, 2] = 7
d[4, 3] = 8

# Decision variables x[i,j] for all directed arcs (i != j)
x = dict()
for i in cities:
    for j in cities:
        if i != j:
            x[i, j] = solver.IntVar(0, 1, 'x_{}_{}'.format(i, j))

# MTZ auxiliary variables u_i for i in {2, 3, 4}
u = dict()
for i in [2, 3, 4]:
    u[i] = solver.NumVar(0, N - 1, 'u_{}'.format(i))

# Objective: minimize total distance
objective = 0
for i in cities:
    for j in cities:
        if i != j:
            objective += d[i, j] * x[i, j]
solver.Minimize(objective)

# Outflow conservation: exactly one outgoing arc per city
for i in cities:
    solver.Add(sum(x[i, j] for j in cities if j != i) == 1)

# Inflow conservation: exactly one incoming arc per city
for j in cities:
    solver.Add(sum(x[i, j] for i in cities if i != j) == 1)

# MTZ subtour elimination constraints for i, j in {2, 3, 4}, i != j
for i in [2, 3, 4]:
    for j in [2, 3, 4]:
        if i != j:
            solver.Add(u[i] - u[j] + N * x[i, j] <= N - 1)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")