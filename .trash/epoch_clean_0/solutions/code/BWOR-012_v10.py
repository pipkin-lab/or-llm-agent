from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Index sets
G = [0, 1, 2]  # grades 1, 2, 3
B = ['R', 'Y', 'Bl']

# Parameters
S = [1500, 2000, 1000]
C = [6.0, 4.5, 3.0]
P = {'R': 5.5, 'Y': 5.0, 'Bl': 4.8}

# Weights for Goal Programming (W1 >> W2 >> W3)
W1 = 1000000.0
W2 = 1000.0
W3 = 1.0

# Decision variables
# x[g][b] : amount of grade g in brand b
x = dict()
for g in G:
    for b in B:
        x[g, b] = solver.NumVar(0, inf, 'x_' + str(g) + '_' + b)

# X[b] : total production of brand b
X = dict()
for b in B:
    X[b] = solver.NumVar(0, inf, 'X_' + b)

# Deviation variables for Goal 1 (blending)
# Lower bounds: (1, R), (1, Y), (1, Bl)
# Upper bounds: (3, R), (3, Y), (3, Bl)
d_L_minus = dict()
d_L_plus = dict()
d_U_minus = dict()
d_U_plus = dict()

for (g, b) in [(1, 'R'), (1, 'Y'), (1, 'Bl')]:
    key = (g, b)
    d_L_minus[key] = solver.NumVar(0, inf, 'dLm_' + str(g) + '_' + b)
    d_L_plus[key] = solver.NumVar(0, inf, 'dLp_' + str(g) + '_' + b)

for (g, b) in [(3, 'R'), (3, 'Y'), (3, 'Bl')]:
    key = (g, b)
    d_U_minus[key] = solver.NumVar(0, inf, 'dUm_' + str(g) + '_' + b)
    d_U_plus[key] = solver.NumVar(0, inf, 'dUp_' + str(g) + '_' + b)

# Deviation variables for Goal 3 (Red production)
d_R_prod_minus = solver.NumVar(0, inf, 'dR_prod_m')
d_R_prod_plus = solver.NumVar(0, inf, 'dR_prod_p')

# Constraints

# 1. Supply constraints
for g in G:
    solver.Add(sum(x[g, b] for b in B) <= S[g])

# 2. Definition of X[b]
for b in B:
    solver.Add(X[b] == sum(x[g, b] for g in G))

# 3. Goal 1: Blending proportions
# Lower bounds
solver.Add(x[1, 'R'] - 0.5 * X['R'] + d_L_minus[(1, 'R')] - d_L_plus[(1, 'R')] == 0)
solver.Add(x[1, 'Y'] - 0.2 * X['Y'] + d_L_minus[(1, 'Y')] - d_L_plus[(1, 'Y')] == 0)
solver.Add(x[1, 'Bl'] - 0.1 * X['Bl'] + d_L_minus[(1, 'Bl')] - d_L_plus[(1, 'Bl')] == 0)

# Upper bounds
solver.Add(x[3, 'R'] - 0.1 * X['R'] + d_U_minus[(3, 'R')] - d_U_plus[(3, 'R')] == 0)
solver.Add(x[3, 'Y'] - 0.7 * X['Y'] + d_U_minus[(3, 'Y')] - d_U_plus[(3, 'Y')] == 0)
solver.Add(x[3, 'Bl'] - 0.5 * X['Bl'] + d_U_minus[(3, 'Bl')] - d_U_plus[(3, 'Bl')] == 0)

# 4. Goal 3: Red production target
solver.Add(X['R'] + d_R_prod_minus - d_R_prod_plus == 2000)

# Objective Function
# Minimize W1 * (sum of blending deviations) - W2 * (Profit) + W3 * (d_R_prod_minus)

# Blending deviations (only the ones we penalize: d_L_minus and d_U_plus)
blending_dev = (d_L_minus[(1, 'R')] + d_L_minus[(1, 'Y')] + d_L_minus[(1, 'Bl')] +
                d_U_plus[(3, 'R')] + d_U_plus[(3, 'Y')] + d_U_plus[(3, 'Bl')])

# Profit = sum(P[b] * X[b]) - sum(C[g] * sum_b x[g,b])
profit = 0
for b in B:
    profit += P[b] * X[b]
for g in G:
    for b in B:
        profit -= C[g] * x[g, b]

# Goal 3 deviation
goal3_dev = d_R_prod_minus

# Total objective
obj = W1 * blending_dev - W2 * profit + W3 * goal3_dev

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")