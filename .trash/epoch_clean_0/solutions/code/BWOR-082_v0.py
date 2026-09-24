from ortools.linear_solver import pywraplp

# Define the solver (MILP since we have binary variables)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
W = ['A', 'B', 'C', 'D', 'E']
L = ['U', 'alpha', 'beta']
W_pair = [('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E')]

# Parameters
# S_{i, l}: Annual cost savings (in 10,000 yuan/year)
S = {
    ('A', 'alpha'): 100, ('B', 'alpha'): 150, ('C', 'alpha'): 100, ('D', 'alpha'): 200, ('E', 'alpha'): 50,
    ('A', 'beta'): 100, ('B', 'beta'): 200, ('C', 'beta'): 150, ('D', 'beta'): 150, ('E', 'beta'): 150
}
# S_{i, U} = 0 for all i

# C_{ik}: Annual transport volume (tons/year)
C = {
    ('A', 'C'): 1000,
    ('A', 'D'): 1500,
    ('B', 'C'): 1400,
    ('B', 'D'): 1200,
    ('C', 'E'): 2000,
    ('D', 'E'): 700
}

# D_{j, l}: Transportation cost per ton (yuan/t)
D = {
    ('U', 'alpha'): 1300, ('U', 'beta'): 900, ('U', 'U'): 1000,
    ('alpha', 'beta'): 1400, ('alpha', 'U'): 1300, ('alpha', 'alpha'): 500,
    ('beta', 'U'): 900, ('beta', 'alpha'): 1400, ('beta', 'beta'): 500
}

# Decision Variables

# x_{i, l}: Binary variable - 1 if workshop i is at location l
x = dict()
for i in W:
    for l in L:
        x[i, l] = solver.BoolVar('x_' + i + '_' + l)

# y_{i, k, j, l}: Binary variable - 1 if workshop i is at j AND workshop k is at l
# Only for pairs (i, k) in W_pair
y = dict()
for (i, k) in W_pair:
    for j in L:
        for l in L:
            y[i, k, j, l] = solver.BoolVar('y_' + i + '_' + k + '_' + j + '_' + l)

# Constraints

# 1. Assignment Constraint: Each workshop must be assigned to exactly one location
for i in W:
    solver.Add(sum(x[i, l] for l in L) == 1)

# 2. Capacity Constraint: No more than 3 workshops in any location
for l in L:
    solver.Add(sum(x[i, l] for i in W) <= 3)

# 3. Linking Constraints (Linearization of Product)
for (i, k) in W_pair:
    for j in L:
        for l in L:
            # y_{i,k,j,l} <= x_{i,j}
            solver.Add(y[i, k, j, l] <= x[i, j])
            # y_{i,k,j,l} <= x_{k,l}
            solver.Add(y[i, k, j, l] <= x[k, l])
            # y_{i,k,j,l} >= x_{i,j} + x_{k,l} - 1
            solver.Add(y[i, k, j, l] >= x[i, j] + x[k, l] - 1)

# Objective Function
# Minimize Z = sum_{(i,k) in W_pair} C_{ik} * sum_{j in L} sum_{l in L} D_{j,l} * y_{i,k,j,l}
#             - sum_{i in W} sum_{l in L} S_{i,l}^{(yuan)} * x_{i,l}

# Transport cost part
transport_cost = 0
for (i, k) in W_pair:
    for j in L:
        for l in L:
            transport_cost += C[(i, k)] * D[(j, l)] * y[i, k, j, l]

# Savings part (in yuan)
savings = 0
for i in W:
    for l in L:
        if (i, l) in S:
            savings += S[(i, l)] * 10000 * x[i, l]
        else:
            # S_{i, U} = 0
            pass

# Net cost to minimize
objective = transport_cost - savings
solver.Minimize(objective)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")