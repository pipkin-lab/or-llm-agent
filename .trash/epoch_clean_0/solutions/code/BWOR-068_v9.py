from ortools.linear_solver import pywraplp

# Initialize MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
months = [1, 2, 3, 4, 5, 6]
quantities = [10, 20, 30, 40, 50]

# Parameters
D = dict()
D[1] = 40
D[2] = 20
D[3] = 30
D[4] = 40
D[5] = 30
D[6] = 20

K = 10

C_q = dict()
C_q[10] = 48
C_q[20] = 86
C_q[30] = 118
C_q[40] = 138
C_q[50] = 160

h = 0.2
I_max = 40
I_0 = 0

# Decision variables
x = dict()
for t in months:
    for q in quantities:
        x[t, q] = solver.BoolVar('x_' + str(t) + '_' + str(q))

y = dict()
for t in months:
    y[t] = solver.BoolVar('y_' + str(t))

I = dict()
for t in months:
    I[t] = solver.NumVar(0, I_max, 'I_' + str(t))

# Objective function
obj = 0
for t in months:
    for q in quantities:
        obj += C_q[q] * x[t, q]
    obj += K * y[t]
    obj += h * I[t]

solver.Minimize(obj)

# Constraint 1: At most one order quantity per month
for t in months:
    solver.Add(sum(x[t, q] for q in quantities) <= 1)

# Constraint 2: Fixed cost linkage
for t in months:
    for q in quantities:
        solver.Add(y[t] >= x[t, q])

# Constraint 3: Inventory balance
for t in months:
    if t == 1:
        prev_I = I_0
    else:
        prev_I = I[t - 1]
    solver.Add(I[t] == prev_I + sum(q * x[t, q] for q in quantities) - D[t])

# Constraint 4: Inventory capacity (already enforced by variable bounds, but add explicitly for clarity)
for t in months:
    solver.Add(I[t] <= I_max)

# Constraint 5: Final inventory condition
solver.Add(I[6] == 0)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")