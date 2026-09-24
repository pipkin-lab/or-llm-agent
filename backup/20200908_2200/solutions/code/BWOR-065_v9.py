from ortools.linear_solver import pywraplp

# Define the solver (MILP because of binary variables y_t)
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    print("Could not create solver")
    exit(1)

# Index set
months = [1, 2, 3, 4, 5, 6]
n = len(months)

# Parameters
D = dict()
D[1] = 1
D[2] = 2
D[3] = 5
D[4] = 3
D[5] = 2
D[6] = 1

C_prod = 10000
C_fixed = 4000
C_hold = 1000
K_prod = 4
K_store = 3

# Decision variables
x = dict()
I = dict()
y = dict()

for t in months:
    x[t] = solver.NumVar(0, solver.infinity(), 'x_' + str(t))
    I[t] = solver.NumVar(0, solver.infinity(), 'I_' + str(t))
    y[t] = solver.BoolVar('y_' + str(t))

# Constraints

# 1. Inventory balance: I_t = I_{t-1} + x_t - D_t, with I_0 = 0
for t in months:
    if t == 1:
        solver.Add(I[t] == x[t] - D[t])
    else:
        solver.Add(I[t] == I[t-1] + x[t] - D[t])

# 2. Final inventory constraint
solver.Add(I[6] == 0)

# 3. Production capacity constraints
for t in months:
    solver.Add(x[t] <= K_prod)

# 4. Storage capacity constraints
for t in months:
    if t <= 5:
        solver.Add(I[t] <= K_store)
    else:
        solver.Add(I[t] <= K_store)  # I[6] is already 0

# 5. Big-M linking constraints: x_t <= M * y_t, with M = 4
M = 4
for t in months:
    solver.Add(x[t] <= M * y[t])

# Objective function
objective = 0
for t in months:
    objective += C_prod * x[t] + C_fixed * y[t] + C_hold * I[t]

solver.Minimize(objective)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")