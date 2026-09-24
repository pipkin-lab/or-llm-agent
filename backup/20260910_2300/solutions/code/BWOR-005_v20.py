from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets
C = [1, 2, 3]
K = [1, 2, 3]

# Parameters
W = dict()
W[1] = 2000
W[2] = 3000
W[3] = 1500

V = dict()
V[1] = 4000
V[2] = 5000
V[3] = 1500

Q = dict()
Q[1] = 600
Q[2] = 1000
Q[3] = 800

v = dict()
v[1] = 10
v[2] = 5
v[3] = 7

w = dict()
w[1] = 8
w[2] = 6
w[3] = 4

r = dict()
r[1] = 1000
r[2] = 700
r[3] = 600

# Decision variables x[i, k]
x = dict()
for i in C:
    for k in K:
        x[i, k] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(k))

# Objective: Maximize revenue
obj = 0
for i in C:
    for k in K:
        obj += r[i] * x[i, k]

solver.Maximize(obj)

# 1. Supply constraints
for i in C:
    solver.Add(sum(x[i, k] for k in K) <= Q[i])

# 2. Volume capacity constraints
for k in K:
    solver.Add(sum(v[i] * x[i, k] for i in C) <= V[k])

# 3. Weight capacity constraints
for k in K:
    solver.Add(sum(w[i] * x[i, k] for i in C) <= W[k])

# Helper: actual weight in compartment k
def W_actual(k):
    return sum(w[i] * x[i, k] for i in C)

# 4. Balance constraints
# A. Front/Middle: R12 = 2/3, delta = 0.15
# Lower: (2/3)*(1-0.15) = 0.5667
# Upper: (2/3)*(1+0.15) = 0.7667
solver.Add(W_actual(1) - 0.7667 * W_actual(2) <= 0)
solver.Add(W_actual(1) - 0.5667 * W_actual(2) >= 0)

# B. Rear/Middle: R32 = 0.5, delta = 0.15
# Lower: 0.5*(1-0.15) = 0.425
# Upper: 0.5*(1+0.15) = 0.575
solver.Add(W_actual(3) - 0.575 * W_actual(2) <= 0)
solver.Add(W_actual(3) - 0.425 * W_actual(2) >= 0)

# C. Front/Rear: R13 = 4/3, delta = 0.10
# Lower: (4/3)*(1-0.10) = 1.2
# Upper: (4/3)*(1+0.10) = 1.4667
solver.Add(W_actual(1) - 1.4667 * W_actual(3) <= 0)
solver.Add(W_actual(1) - 1.2 * W_actual(3) >= 0)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")