from ortools.linear_solver import pywraplp

# Index sets
products = [1, 2, 3]
stages = [1, 2, 3]

# Parameters
D = dict()
D[1, 1] = 500
D[1, 2] = 680
D[1, 3] = 800
D[2, 1] = 750
D[2, 2] = 800
D[2, 3] = 950
D[3, 1] = 900
D[3, 2] = 800
D[3, 3] = 1000

a_eq = dict()
a_eq[1] = 2.0
a_eq[2] = 1.0
a_eq[3] = 3.1

a_cap = dict()
a_cap[1] = 40
a_cap[2] = 20
a_cap[3] = 55

R_eq = 5000
R_cap = 93000

w = dict()
w[1] = 1
w[2] = 1
w[3] = 2

# Create solver (LP)
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
I = dict()
n = dict()
p = dict()
d_eq_plus = dict()
d_eq_minus = dict()
d_cap_plus = dict()
d_cap_minus = dict()

for i in products:
    for t in stages:
        x[i, t] = solver.NumVar(0, INF, 'x_%d_%d' % (i, t))
        I[i, t] = solver.NumVar(0, INF, 'I_%d_%d' % (i, t))
        n[i, t] = solver.NumVar(0, INF, 'n_%d_%d' % (i, t))
        p[i, t] = solver.NumVar(0, INF, 'p_%d_%d' % (i, t))

for t in stages:
    d_eq_plus[t] = solver.NumVar(0, INF, 'd_eq_plus_%d' % t)
    d_eq_minus[t] = solver.NumVar(0, INF, 'd_eq_minus_%d' % t)
    d_cap_plus[t] = solver.NumVar(0, INF, 'd_cap_plus_%d' % t)
    d_cap_minus[t] = solver.NumVar(0, INF, 'd_cap_minus_%d' % t)

# Constraints

# 1. Inventory Balance: x[i,t] + I[i,t-1] - n[i,t] + p[i,t] = D[i,t] + I[i,t]
for i in products:
    for t in stages:
        if t == 1:
            solver.Add(x[i, 1] - n[i, 1] + p[i, 1] == D[i, 1] + I[i, 1])
        else:
            solver.Add(x[i, t] + I[i, t - 1] - n[i, t] + p[i, t] == D[i, t] + I[i, t])

# Boundary condition: I[i,3] = 0
for i in products:
    solver.Add(I[i, 3] == 0)

# 2. Equipment Resource Goal: sum_i a_eq[i] * x[i,t] - d_eq_minus[t] + d_eq_plus[t] = R_eq
for t in stages:
    expr_eq = sum(a_eq[i] * x[i, t] for i in products)
    solver.Add(expr_eq - d_eq_minus[t] + d_eq_plus[t] == R_eq)

# 3. Working Capital Resource Goal: sum_i a_cap[i] * x[i,t] - d_cap_minus[t] + d_cap_plus[t] = R_cap
for t in stages:
    expr_cap = sum(a_cap[i] * x[i, t] for i in products)
    solver.Add(expr_cap - d_cap_minus[t] + d_cap_plus[t] == R_cap)

# Lexicographic (pre-emptive) solving
# Phase 1: Minimize Z1 = sum_t sum_i w[i] * n[i,t]
z1_expr = sum(w[i] * n[i, t] for t in stages for i in products)
solver.Minimize(z1_expr)
status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
    print("NO_FEASIBLE_SOLUTION")
    exit(0)
z1_val = solver.Objective().Value()
solver.Add(z1_expr == z1_val)

# Phase 2: Minimize Z2 = sum_t d_eq_plus[t]
z2_expr = sum(d_eq_plus[t] for t in stages)
solver.Minimize(z2_expr)
status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
    print("NO_FEASIBLE_SOLUTION")
    exit(0)
z2_val = solver.Objective().Value()
solver.Add(z2_expr == z2_val)

# Phase 3: Minimize Z3 = sum_t d_cap_plus[t]
z3_expr = sum(d_cap_plus[t] for t in stages)
solver.Minimize(z3_expr)
status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
    print("NO_FEASIBLE_SOLUTION")
    exit(0)

z3_val = solver.Objective().Value()

# The problem asks for the final priority-3 objective value
print("OPTIMAL_VALUE:", z3_val)