from ortools.linear_solver import pywraplp

# Define sets
W = ['A', 'B', 'C', 'D', 'E']
L = ['U', 'alpha', 'beta']

# Parameters: Savings (in yuan)
# S[i][l]
S = {
    'A': {'U': 0, 'alpha': 1000000, 'beta': 1000000},
    'B': {'U': 0, 'alpha': 1500000, 'beta': 2000000},
    'C': {'U': 0, 'alpha': 1000000, 'beta': 1500000},
    'D': {'U': 0, 'alpha': 2000000, 'beta': 1500000},
    'E': {'U': 0, 'alpha': 500000, 'beta': 1500000}
}

# Parameters: Transport Volumes C[i][k] (tons)
# Symmetric, define for i < k based on index order in W
C = {}
pairs = [
    ('A', 'C', 1000),
    ('A', 'D', 1500),
    ('B', 'C', 1400),
    ('B', 'D', 1200),
    ('C', 'E', 2000),
    ('D', 'E', 700)
]
for i, k, val in pairs:
    C[(i, k)] = val
    C[(k, i)] = val

# Parameters: Transport Costs D[j][l] (yuan/ton)
D = {
    'U': {'U': 1000, 'alpha': 1300, 'beta': 900},
    'alpha': {'U': 1300, 'alpha': 500, 'beta': 1400},
    'beta': {'U': 900, 'alpha': 1400, 'beta': 500}
}

# Capacity
M = 3

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    print("Could not create solver")
    exit(1)

# Decision Variables
# x[i][l]: 1 if workshop i is at location l
x = dict()
for i in W:
    for l in L:
        x[i, l] = solver.IntVar(0, 1, 'x_' + i + '_' + l)

# y[i][k][j][l]: 1 if workshop i is at j AND workshop k is at l
# Only needed for pairs (i, k) where C[i][k] > 0 and i != k
# To avoid double counting in objective, we will sum over unique pairs (i, k) where i < k in the list W
# But we need y for the linearization.
# Let's create y for all ordered pairs (i, k) where i != k, but only use them in objective for i < k.
# Actually, for linearization, we can just create y for all i != k.
y = dict()
for i in W:
    for k in W:
        if i == k:
            continue
        for j in L:
            for l in L:
                y[i, k, j, l] = solver.IntVar(0, 1, 'y_' + i + '_' + k + '_' + j + '_' + l)

# Constraints

# 1. Assignment: Each workshop is in exactly one location
for i in W:
    solver.Add(sum(x[i, l] for l in L) == 1)

# 2. Capacity: Max M workshops per location
for l in L:
    solver.Add(sum(x[i, l] for i in W) <= M)

# 3. Linking constraints for y
# y[i, k, j, l] <= x[i, j]
# y[i, k, j, l] <= x[k, l]
# y[i, k, j, l] >= x[i, j] + x[k, l] - 1
for i in W:
    for k in W:
        if i == k:
            continue
        for j in L:
            for l in L:
                solver.Add(y[i, k, j, l] <= x[i, j])
                solver.Add(y[i, k, j, l] <= x[k, l])
                solver.Add(y[i, k, j, l] >= x[i, j] + x[k, l] - 1)

# Objective Function
# Minimize Total Transport Cost - Total Savings
# Transport Cost: Sum over unique pairs (i, k) with i < k of C[i][k] * (Sum_{j,l} D[j][l] * y[i, k, j, l])
# Note: y[i, k, j, l] is 1 if i is at j and k is at l.
# We sum over i, k in W where i < k.
obj = 0

# Add Transport Costs
for i_idx in range(len(W)):
    for k_idx in range(i_idx + 1, len(W)):
        i = W[i_idx]
        k = W[k_idx]
        if (i, k) in C:
            vol = C[(i, k)]
            # Sum over all location pairs j, l
            # y[i, k, j, l] is defined
            transport_cost_term = 0
            for j in L:
                for l in L:
                    transport_cost_term += D[j][l] * y[i, k, j, l]
            obj += vol * transport_cost_term

# Subtract Savings
for i in W:
    for l in L:
        obj -= S[i][l] * x[i, l]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")