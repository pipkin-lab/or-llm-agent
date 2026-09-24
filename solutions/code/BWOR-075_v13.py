from ortools.linear_solver import pywraplp

# Node set: 0 = Coast, 1-8 = Wells
V = list(range(9))
n = len(V)
root = 0

# Edge costs (undirected), stored in a dict keyed by (i, j) with i < j
cost = dict()
cost[(0, 1)] = 5.0
cost[(1, 2)] = 1.3
cost[(1, 3)] = 2.1
cost[(1, 4)] = 0.9
cost[(1, 5)] = 0.7
cost[(1, 6)] = 1.8
cost[(1, 7)] = 2.0
cost[(1, 8)] = 1.5
cost[(2, 3)] = 0.9
cost[(2, 4)] = 1.8
cost[(2, 5)] = 1.2
cost[(2, 6)] = 2.6
cost[(2, 7)] = 2.3
cost[(2, 8)] = 1.1
cost[(3, 4)] = 2.6
cost[(3, 5)] = 1.7
cost[(3, 6)] = 2.5
cost[(3, 7)] = 1.9
cost[(3, 8)] = 1.0
cost[(4, 5)] = 0.7
cost[(4, 6)] = 1.6
cost[(4, 7)] = 1.5
cost[(4, 8)] = 0.9
cost[(5, 6)] = 0.9
cost[(5, 7)] = 1.1
cost[(5, 8)] = 0.8
cost[(6, 7)] = 0.6
cost[(6, 8)] = 1.0
cost[(7, 8)] = 0.5

# Build list of undirected edges
edges = list(cost.keys())

# Solver: MILP -> SCIP
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables:
# z[i, j] binary, 1 if arc i -> j is used (directed representation)
# We only need arcs between all ordered pairs i != j
z = dict()
for i in V:
    for j in V:
        if i != j:
            z[i, j] = solver.BoolVar('z_' + str(i) + '_' + str(j))

# Ordering variables u_i for MTZ subtour elimination
# u_0 fixed to 0, u_i in [0, n-1] for i != 0
u = dict()
u[root] = solver.NumVar(0, 0, 'u_' + str(root))
for i in V:
    if i != root:
        u[i] = solver.NumVar(0, n - 1, 'u_' + str(i))

# Objective: minimize total pipeline length
# For each undirected edge (i, j), cost is c_ij * (z[i,j] + z[j,i])
obj_terms = []
for (i, j) in edges:
    c = cost[(i, j)]
    obj_terms.append(c * (z[i, j] + z[j, i]))

solver.Minimize(sum(obj_terms))

# Constraint 1: Out-degree of root = 1
out_root_expr = sum(z[root, j] for j in V if j != root)
solver.Add(out_root_expr == 1)

# Constraint 2: Flow conservation for non-root nodes (exactly one incoming arc)
for i in V:
    if i != root:
        in_expr = sum(z[j, i] for j in V if j != i)
        solver.Add(in_expr == 1)

# Constraint 3: MTZ subtour elimination
# For all i, j in V \ {root}, i != j:
#   u_i - u_j + n * z[i, j] <= n - 1
for i in V:
    if i == root:
        continue
    for j in V:
        if j == root or j == i:
            continue
        solver.Add(u[i] - u[j] + n * z[i, j] <= n - 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")