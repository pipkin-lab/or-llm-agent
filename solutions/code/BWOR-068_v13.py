from ortools.linear_solver import pywraplp

# Parameters
T = [1, 2, 3, 4, 5, 6]  # Months 1-6
K = [1, 2, 3, 4, 5]     # Order size options 1-5

D = dict()
D[1] = 40
D[2] = 20
D[3] = 30
D[4] = 40
D[5] = 30
D[6] = 20

q = dict()
q[1] = 10
q[2] = 20
q[3] = 30
q[4] = 40
q[5] = 50

c = dict()
c[1] = 48
c[2] = 86
c[3] = 118
c[4] = 138
c[5] = 160

f_fixed = 10
h = 0.2
I_max = 40
I_0 = 0
I_final = 0

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for t in T:
    for k in K:
        x[t, k] = solver.BoolVar('x_{}_{}'.format(t, k))

y = dict()
for t in T:
    y[t] = solver.BoolVar('y_{}'.format(t))

I = dict()
for t in T:
    I[t] = solver.IntVar(0, I_max, 'I_{}'.format(t))

# Objective
obj_terms = []
for t in T:
    for k in K:
        obj_terms.append(c[k] * x[t, k])
    obj_terms.append(f_fixed * y[t])
    obj_terms.append(h * I[t])

solver.Minimize(sum(obj_terms))

# Constraint 1: At most one order size per month
for t in T:
    solver.Add(sum(x[t, k] for k in K) <= 1)

# Constraint 2: Setup activation
for t in T:
    for k in K:
        solver.Add(y[t] >= x[t, k])

# Constraint 3: Inventory balance
for t in T:
    if t == 1:
        solver.Add(I[1] == I_0 + sum(q[k] * x[1, k] for k in K) - D[1])
    else:
        prev_t = t - 1
        solver.Add(I[t] == I[prev_t] + sum(q[k] * x[t, k] for k in K) - D[t])

# I_6 = 0
solver.Add(I[6] == I_final)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")