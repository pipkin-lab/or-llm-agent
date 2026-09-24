from ortools.linear_solver import pywraplp

# Define sets
W = ['A', 'B', 'C', 'D', 'E']
L = ['alpha', 'beta', 'U']
L_idx = {loc: idx for idx, loc in enumerate(L)}

# Parameters
# Savings S_ij (10,000 yuan/year)
S = {
    ('A', 'alpha'): 100, ('A', 'beta'): 100, ('A', 'U'): 0,
    ('B', 'alpha'): 150, ('B', 'beta'): 200, ('B', 'U'): 0,
    ('C', 'alpha'): 100, ('C', 'beta'): 150, ('C', 'U'): 0,
    ('D', 'alpha'): 200, ('D', 'beta'): 150, ('D', 'U'): 0,
    ('E', 'alpha'): 50,  ('E', 'beta'): 150, ('E', 'U'): 0,
}

# Transportation Volume C_ik (tons/year) - symmetric
C = {
    ('A', 'B'): 0,    ('A', 'C'): 1000, ('A', 'D'): 1500, ('A', 'E'): 0,
    ('B', 'C'): 1400, ('B', 'D'): 1200, ('B', 'E'): 0,
    ('C', 'D'): 0,    ('C', 'E'): 2000,
    ('D', 'E'): 700
}

# Transportation Cost D_jl (yuan/ton) - symmetric
D = {
    ('alpha', 'alpha'): 500, ('alpha', 'beta'): 1400, ('alpha', 'U'): 1300,
    ('beta', 'beta'): 500,   ('beta', 'U'): 900,
    ('U', 'U'): 1000
}

# Helper to get symmetric values
def get_C(i, k):
    if i == k:
        return 0
    if (i, k) in C:
        return C[(i, k)]
    else:
        return C[(k, i)]

def get_D(j, l):
    if (j, l) in D:
        return D[(j, l)]
    else:
        return D[(l, j)]

# Create Solver (MILP because of binary variables)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision Variables
# x[i][j] is 1 if workshop i is at location j
x = dict()
for i in W:
    for j in L:
        x[i, j] = solver.BoolVar('x_' + i + '_' + j)

# y[i][k][j][l] is 1 if workshop i is at j AND workshop k is at l
# Only for i < k to avoid double counting in objective, but constraints need to handle all pairs?
# The model says: y_ijkl for i, k in W with i < k, j, l in L.
# Wait, the linking constraints usually apply to the specific pair (i,k).
# Let's define y for all i < k.
y = dict()
for idx_i, i in enumerate(W):
    for idx_k, k in enumerate(W):
        if idx_i < idx_k: # i < k
            for j in L:
                for l in L:
                    y[i, k, j, l] = solver.BoolVar('y_' + i + '_' + k + '_' + j + '_' + l)

# Objective Function
# Minimize: sum( (C_ik * D_jl / 10000) * y_ijkl ) - sum( S_ij * x_ij )
obj_terms = []

# Transport cost part
for idx_i, i in enumerate(W):
    for idx_k, k in enumerate(W):
        if idx_i < idx_k:
            c_val = get_C(i, k)
            if c_val == 0:
                continue
            for j in L:
                for l in L:
                    d_val = get_D(j, l)
                    coeff = (c_val * d_val) / 10000.0
                    obj_terms.append(coeff * y[i, k, j, l])

# Savings part (subtracted, so negative in minimization)
for i in W:
    for j in L:
        s_val = S[(i, j)]
        obj_terms.append(-s_val * x[i, j])

solver.Minimize(sum(obj_terms))

# Constraints

# 1. Assignment: Each workshop i is in exactly one location
for i in W:
    solver.Add(sum(x[i, j] for j in L) == 1)

# 2. Capacity: No more than 3 workshops in any location
for j in L:
    solver.Add(sum(x[i, j] for i in W) <= 3)

# 3. Linking Constraints for y_ijkl
# y_ijkl <= x_ij
# y_ijkl <= x_kl
# y_ijkl >= x_ij + x_kl - 1
for idx_i, i in enumerate(W):
    for idx_k, k in enumerate(W):
        if idx_i < idx_k:
            for j in L:
                for l in L:
                    var_y = y[i, k, j, l]
                    var_xi = x[i, j]
                    var_xk = x[k, l]
                    
                    solver.Add(var_y <= var_xi)
                    solver.Add(var_y <= var_xk)
                    solver.Add(var_y >= var_xi + var_xk - 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")