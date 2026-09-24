from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
V = list(range(1, 9))  # Wells 1 to 8
N = len(V)

# Distance parameters (symmetric)
# d[i][j] where i, j in 1..8
d = {}
distances = {
    (1, 2): 1.3, (1, 3): 2.1, (1, 4): 0.9, (1, 5): 0.7, (1, 6): 1.8, (1, 7): 2.0, (1, 8): 1.5,
    (2, 3): 0.9, (2, 4): 1.8, (2, 5): 1.2, (2, 6): 2.6, (2, 7): 2.3, (2, 8): 1.1,
    (3, 4): 2.6, (3, 5): 1.7, (3, 6): 2.5, (3, 7): 1.9, (3, 8): 1.0,
    (4, 5): 0.7, (4, 6): 1.6, (4, 7): 1.5, (4, 8): 0.9,
    (5, 6): 0.9, (5, 7): 1.1, (5, 8): 0.8,
    (6, 7): 0.6, (6, 8): 1.0,
    (7, 8): 0.5
}

for i, j in distances:
    d[(i, j)] = distances[(i, j)]
    d[(j, i)] = distances[(i, j)]

# Decision variables
# x[i, j] binary: pipeline from i to j
x = dict()
for i in V:
    for j in V:
        if i != j:
            x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# u[i] continuous auxiliary variables for nodes 2..8
u = dict()
for i in V:
    if i != 1:
        u[i] = solver.NumVar(0, N - 1, 'u_' + str(i))

# Objective: Minimize total pipeline length including the fixed 5 miles from coast to well 1
obj = solver.Sum(d[(i, j)] * x[i, j] for i in V for j in V if i != j)
# Add the constant 5 miles
solver.Minimize(obj + 5)

# Flow Conservation / Tree Structure Constraints
# Root (node 1): no incoming flow
solver.Add(solver.Sum(x[i, 1] for i in V if i != 1) == 0)

# Every other node has exactly one incoming connection
for j in V:
    if j != 1:
        solver.Add(solver.Sum(x[i, j] for i in V if i != j) == 1)

# MTZ Subtour Elimination Constraints
# For all i, j in {2, 3, 4, 5, 6, 7, 8} with i != j:
# u_i - u_j + N * x_ij <= N - 1
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