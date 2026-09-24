from ortools.linear_solver import pywraplp

# Parameters
P = [1, 2, 3]
T = [1, 2, 3]

D = dict()
D[1, 1] = 500
D[2, 1] = 750
D[3, 1] = 900
D[1, 2] = 680
D[2, 2] = 800
D[3, 2] = 800
D[1, 3] = 800
D[2, 3] = 950
D[3, 3] = 1000

a = dict()
a[1] = 2.0
a[2] = 1.0
a[3] = 3.1

b = dict()
b[1] = 40
b[2] = 20
b[3] = 55

H = 5000
W = 93000

w = dict()
w[1] = 1
w[2] = 1
w[3] = 2

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
for p in P:
    for t in T:
        x[p, t] = solver.NumVar(0, INF, 'x_' + str(p) + '_' + str(t))

s_minus = dict()
for p in P:
    for t in T:
        s_minus[p, t] = solver.NumVar(0, INF, 's_minus_' + str(p) + '_' + str(t))

s_plus = dict()
for p in P:
    for t in T:
        s_plus[p, t] = solver.NumVar(0, INF, 's_plus_' + str(p) + '_' + str(t))

e_minus = dict()
for t in T:
    e_minus[t] = solver.NumVar(0, INF, 'e_minus_' + str(t))

e_plus = dict()
for t in T:
    e_plus[t] = solver.NumVar(0, INF, 'e_plus_' + str(t))

c_minus = dict()
for t in T:
    c_minus[t] = solver.NumVar(0, INF, 'c_minus_' + str(t))

c_plus = dict()
for t in T:
    c_plus[t] = solver.NumVar(0, INF, 'c_plus_' + str(t))

# Demand balance constraints
for p in P:
    for t in T:
        solver.Add(x[p, t] + s_minus[p, t] - s_plus[p, t] == D[p, t])

# Equipment hours balance constraints
for t in T:
    expr = sum(a[p] * x[p, t] for p in P) + e_minus[t] - e_plus[t]
    solver.Add(expr == H)

# Working capital balance constraints
for t in T:
    expr = sum(b[p] * x[p, t] for p in P) + c_minus[t] - c_plus[t]
    solver.Add(expr == W)

# Priority 1: Minimize weighted stockouts
Z1_terms = sum(w[p] * s_minus[p, t] for p in P for t in T)
solver.Minimize(Z1_terms)

status = solver.Solve()
if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
    print("NO_FEASIBLE_SOLUTION")
else:
    Z1_star = solver.Objective().Value()
    solver.Add(Z1_terms == Z1_star)

    # Priority 2: Minimize equipment overloading
    Z2_terms = sum(e_plus[t] for t in T)
    solver.Minimize(Z2_terms)

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
        print("NO_FEASIBLE_SOLUTION")
    else:
        Z2_star = solver.Objective().Value()
        solver.Add(Z2_terms == Z2_star)

        # Priority 3: Minimize working capital excess
        Z3_terms = sum(c_plus[t] for t in T)
        solver.Minimize(Z3_terms)

        status = solver.Solve()
        if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
            print("NO_FEASIBLE_SOLUTION")
        else:
            Z3_star = solver.Objective().Value()
            print("OPTIMAL_VALUE:", Z3_star)