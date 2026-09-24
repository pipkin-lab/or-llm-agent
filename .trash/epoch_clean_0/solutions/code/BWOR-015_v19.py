from ortools.linear_solver import pywraplp

# Define sets and parameters
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

H_max = 5000
C_max = 93000

weights = dict()
weights[1] = 1
weights[2] = 1
weights[3] = 2

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x = dict()
for p in P:
    for t in T:
        x[p, t] = solver.NumVar(0, INF, 'x_' + str(p) + '_' + str(t))

I = dict()
for p in P:
    for t in T:
        I[p, t] = solver.NumVar(0, INF, 'I_' + str(p) + '_' + str(t))

s = dict()
for p in P:
    for t in T:
        s[p, t] = solver.NumVar(0, INF, 's_' + str(p) + '_' + str(t))

e_plus = dict()
for t in T:
    e_plus[t] = solver.NumVar(0, INF, 'e_plus_' + str(t))

e_minus = dict()
for t in T:
    e_minus[t] = solver.NumVar(0, INF, 'e_minus_' + str(t))

# Constraints: Inventory Balance
for p in P:
    # t=1: I[p,1] - s[p,1] = x[p,1] - D[p,1]
    solver.Add(I[p, 1] - s[p, 1] == x[p, 1] - D[p, 1])
    # t=2: I[p,2] - s[p,2] = I[p,1] + x[p,2] - D[p,2]
    solver.Add(I[p, 2] - s[p, 2] == I[p, 1] + x[p, 2] - D[p, 2])
    # t=3: I[p,3] = 0, so -s[p,3] = I[p,2] + x[p,3] - D[p,3]
    solver.Add(0 - s[p, 3] == I[p, 2] + x[p, 3] - D[p, 3])

# Constraints: Equipment Capacity
for t in T:
    solver.Add(sum(a[p] * x[p, t] for p in P) + e_minus[t] - e_plus[t] == H_max)

# Constraints: Working Capital Limit (Hard Constraint)
for t in T:
    solver.Add(sum(b[p] * x[p, t] for p in P) <= C_max)

# Objective 1: Minimize weighted stockouts
Z1 = sum(weights[p] * s[p, t] for p in P for t in T)

# Phase 1: Minimize Z1
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    Z1_val = solver.Objective().Value()
    # Fix Z1 to its optimal value
    solver.Add(Z1 == Z1_val)
    
    # Objective 2: Minimize equipment overload
    Z2 = sum(e_plus[t] for t in T)
    solver.Minimize(Z2)
    
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")
else:
    print("NO_FEASIBLE_SOLUTION")