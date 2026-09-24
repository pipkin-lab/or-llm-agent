from ortools.linear_solver import pywraplp

# Initialize solver for Linear Programming
solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    raise RuntimeError("Solver creation failed")

# Sets
G = [1, 2, 3]  # Grades I, II, III
B = ['R', 'Y', 'B']  # Brands Red, Yellow, Blue

# Parameters
S = {1: 1500, 2: 2000, 3: 1000}
C = {1: 6.0, 2: 4.5, 3: 3.0}
P_price = {'R': 5.5, 'Y': 5.0, 'B': 4.8}
D_min = {'R': 2000, 'Y': 0, 'B': 0}

# Blending bounds (L, U) for each (grade, brand)
# Defaults to (0, 1.0)
L = dict()
U = dict()
for g in G:
    for b in B:
        L[g, b] = 0.0
        U[g, b] = 1.0

# Red
L[1, 'R'] = 0.50
U[1, 'R'] = 1.0
L[2, 'R'] = 0.0
U[2, 'R'] = 1.0
L[3, 'R'] = 0.0
U[3, 'R'] = 0.10

# Yellow
L[1, 'Y'] = 0.20
U[1, 'Y'] = 1.0
L[2, 'Y'] = 0.0
U[2, 'Y'] = 1.0
L[3, 'Y'] = 0.0
U[3, 'Y'] = 0.70

# Blue
L[1, 'B'] = 0.10
U[1, 'B'] = 1.0
L[2, 'B'] = 0.0
U[2, 'B'] = 1.0
L[3, 'B'] = 0.0
U[3, 'B'] = 0.50

# Decision Variables
# x[g, b]: amount of grade g in brand b
x = dict()
for g in G:
    for b in B:
        x[g, b] = solver.NumVar(0, solver.infinity(), 'x_' + str(g) + '_' + b)

# P[b]: total production of brand b
P = dict()
for b in B:
    P[b] = solver.NumVar(0, solver.infinity(), 'P_' + b)

# Constraints
# 1. Production Balance: P[b] = sum_g x[g, b]
for b in B:
    solver.Add(P[b] == sum(x[g, b] for g in G))

# 2. Raw Material Supply Constraints
for g in G:
    solver.Add(sum(x[g, b] for b in B) <= S[g])

# 3. Blending Proportion Constraints
# L[g, b] * P[b] <= x[g, b]  =>  x[g, b] - L[g, b] * P[b] >= 0
# x[g, b] <= U[g, b] * P[b]  =>  x[g, b] - U[g, b] * P[b] <= 0
for g in G:
    for b in B:
        if L[g, b] > 0:
            solver.Add(x[g, b] - L[g, b] * P[b] >= 0)
        if U[g, b] < 1.0:
            solver.Add(x[g, b] - U[g, b] * P[b] <= 0)

# 4. Minimum Production Requirement
for b in B:
    solver.Add(P[b] >= D_min[b])

# Objective Function: Maximize Profit
# Revenue - Cost
revenue = sum(P[b] * P_price[b] for b in B)
cost = sum(x[g, b] * C[g] for g in G for b in B)
solver.Maximize(revenue - cost)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")