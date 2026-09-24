from ortools.linear_solver import pywraplp

# Parameters
# Cities: 1, 2, 3, 4. Start city = 1.
# Distance matrix (1-indexed for clarity, will adjust to 0-indexed internally)
# d[i][j] where i, j are 1..4
d = [
    [0, 6, 7, 9],  # from 1
    [8, 0, 9, 7],  # from 2
    [5, 8, 0, 8],  # from 3
    [6, 5, 5, 0]   # from 4
]

# Since this is a small ATSP (n=4), we can use a MILP formulation with MTZ or subtour elimination.
# Given the instruction to convert the DP model, but OR-Tools pywraplp is an LP/MILP solver,
# we will formulate it as an ATSP MILP.
# n = 4 cities.
n = 4

# We use 0-indexed internally for arrays, but the math model uses 1-indexed.
# Let's stick to 0-indexed for code simplicity: cities 0, 1, 2, 3 corresponding to 1, 2, 3, 4.
# Start city is 0.
start = 0

# Distance matrix 0-indexed
dist = [
    [0, 6, 7, 9],
    [8, 0, 9, 7],
    [5, 8, 0, 8],
    [6, 5, 5, 0]
]

solver = pywraplp.Solver.CreateSolver('SCIP')

# Variables x[i, j] = 1 if arc i->j is in the tour
x = dict()
for i in range(n):
    for j in range(n):
        if i != j:
            x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# MTZ auxiliary variables u[i] for i in 1..n-1 (cities 1, 2, 3 in 0-indexed)
# u[0] is fixed to 0 implicitly by constraints or explicitly.
# We define u for all nodes 0..n-1, but u[0] will be constrained to 0.
u = dict()
for i in range(n):
    u[i] = solver.NumVar(0, n - 1, 'u_' + str(i))

# Fix u[start] = 0
solver.Add(u[start] == 0)

# Degree constraints: each node has exactly one incoming and one outgoing arc
for i in range(n):
    # Outgoing
    solver.Add(sum(x[i, j] for j in range(n) if j != i) == 1)
    # Incoming
    solver.Add(sum(x[j, i] for j in range(n) if j != i) == 1)

# MTZ Subtour Elimination Constraints
# Constraint: u[i] - u[j] + n * x[i, j] <= n - 1
# This is valid for i, j not equal to start?
# Standard MTZ: u[i] - u[j] + n * x[i, j] <= n - 1 for all i, j in V, i != j, i != start, j != start?
# Actually, the standard MTZ formulation for TSP with node 0 as start:
# For all i, j in {1, ..., n-1}, i != j:
#   u[i] - u[j] + n * x[i, j] <= n - 1
# Also, we need to handle arcs leaving/entering start?
# If we fix u[0]=0, and define u for 1..n-1:
# For arc i->j where i,j != 0: u[i] - u[j] + n*x[i,j] <= n-1
# For arc 0->j (j!=0): u[0] - u[j] + n*x[0,j] <= n-1  => -u[j] + n*x[0,j] <= n-1. Since x[0,j] is 0 or 1, and u[j]>=0, this is usually satisfied if u[j] is small, but let's be precise.
# For arc i->0 (i!=0): u[i] - u[0] + n*x[i,0] <= n-1 => u[i] + n*x[i,0] <= n-1.
#
# Let's implement the standard MTZ for ATSP with start node 0.
# Variables u[1]...u[n-1] bounded [1, n-1] or [0, n-1].
# Constraint for all i, j in {1, ..., n-1}, i != j:
#   u[i] - u[j] + n * x[i, j] <= n - 1
#
# Additionally, to ensure the path starts at 0, we rely on the degree constraints.
# The MTZ constraints above prevent subtours not containing 0.
# What about subtours containing 0? They are prevented by the fact that 0 has in/out degree 1 and the path must be a single cycle.
# Wait, MTZ prevents all subtours except the one containing all nodes if applied correctly.
# Let's add constraints for i, j in 1..n-1.

for i in range(1, n):
    for j in range(1, n):
        if i != j:
            solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)

# Objective: Minimize total distance
obj = 0
for i in range(n):
    for j in range(n):
        if i != j:
            obj += dist[i][j] * x[i, j]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")