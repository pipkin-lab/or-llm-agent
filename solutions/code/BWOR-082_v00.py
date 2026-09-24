from ortools.linear_solver import pywraplp

# Define indices
I = ['A', 'B', 'C', 'D', 'E']
J = ['alpha', 'beta', 'Urban']

# Transport volumes C[i][k] in t/year (symmetric)
C = dict()
C[('A', 'B')] = 0
C[('A', 'C')] = 1000
C[('A', 'D')] = 1500
C[('A', 'E')] = 0
C[('B', 'C')] = 1400
C[('B', 'D')] = 1200
C[('B', 'E')] = 0
C[('C', 'D')] = 0
C[('C', 'E')] = 2000
C[('D', 'E')] = 700

# Transport costs D[j][l] in yuan/ton (symmetric)
D = dict()
D[('Urban', 'Urban')] = 1000
D[('alpha', 'alpha')] = 500
D[('beta', 'beta')] = 500
D[('alpha', 'beta')] = 1400
D[('alpha', 'Urban')] = 1300
D[('beta', 'Urban')] = 900

# Savings S[i][j] in 10,000 yuan/year
S = dict()
S[('A', 'alpha')] = 100
S[('B', 'alpha')] = 150
S[('C', 'alpha')] = 100
S[('D', 'alpha')] = 200
S[('E', 'alpha')] = 50
S[('A', 'beta')] = 100
S[('B', 'beta')] = 200
S[('C', 'beta')] = 150
S[('D', 'beta')] = 150
S[('E', 'beta')] = 150

# Create solver (MILP)
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Create binary decision variables x[i][j]
x = dict()
for i in I:
    for j in J:
        x[(i, j)] = solver.BoolVar('x_' + i + '_' + j)

# Create auxiliary variables y[i][k][j][l] = x[i][j] * x[k][l] for i < k
# We need these to linearize the product terms in the objective
# Actually, we can use a simpler approach: for each pair (i,k) with i<k,
# and for each (j,l), we need to represent x[i][j]*x[k][l].
# But the objective is: sum_{i<k} C[i][k] * sum_{j,l} D[j][l] * x[i][j] * x[k][l]
# We can linearize by introducing y[i,k,j,l] for each i<k and j,l
# However, a cleaner approach: for each pair (i,k), the transport cost is
# sum_{j,l} D[j][l] * x[i][j] * x[k][l]
# Let's introduce t[i,k] = sum_{j,l} D[j][l] * x[i][j] * x[k][l]
# But t[i,k] is non-linear. Instead, we can use the fact that x[i][j]*x[k][l]
# can be represented with auxiliary binary variables.

# For each i < k, and for each j, l, define y[i,k,j,l] = x[i,j] * x[k,l]
# y is binary and satisfies:
# y[i,k,j,l] <= x[i,j]
# y[i,k,j,l] <= x[k,l]
# y[i,k,j,l] >= x[i,j] + x[k,l] - 1
# y[i,k,j,l] >= 0

y = dict()
pairs = []
for idx_i, i in enumerate(I):
    for k in I[idx_i + 1:]:
        pairs.append((i, k))

for (i, k) in pairs:
    for j in J:
        for l in J:
            y[(i, k, j, l)] = solver.BoolVar('y_' + i + '_' + k + '_' + j + '_' + l)

# Add constraints for y variables
for (i, k) in pairs:
    for j in J:
        for l in J:
            solver.Add(y[(i, k, j, l)] <= x[(i, j)])
            solver.Add(y[(i, k, j, l)] <= x[(k, l)])
            solver.Add(y[(i, k, j, l)] >= x[(i, j)] + x[(k, l)] - 1)

# Objective: minimize total transport cost (in 10,000 yuan) minus savings
# Transport cost for pair (i,k): sum_{j,l} D[j][l] * y[i,k,j,l] (in yuan)
# Convert to 10,000 yuan: divide by 10000
# C[i][k] is in t/year, D[j][l] in yuan/ton, so C[i][k]*D[j][l] is in yuan/year
# Divide by 10000 to get 10,000 yuan/year

obj = 0
for (i, k) in pairs:
    c_val = C[(i, k)]
    if c_val == 0:
        continue
    for j in J:
        for l in J:
            d_val = D[(j, l)]
            obj += c_val * d_val * y[(i, k, j, l)]

# Subtract savings (already in 10,000 yuan)
for i in I:
    for j in ['alpha', 'beta']:
        obj -= S[(i, j)] * x[(i, j)]

# Convert transport cost from yuan to 10,000 yuan
obj = obj / 10000.0

solver.Minimize(obj)

# Constraint 1: Each workshop in exactly one area
for i in I:
    solver.Add(sum(x[(i, j)] for j in J) == 1)

# Constraint 2: No more than 3 workshops per area
for j in J:
    solver.Add(sum(x[(i, j)] for i in I) <= 3)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")