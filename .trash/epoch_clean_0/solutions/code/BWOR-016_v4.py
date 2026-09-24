from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    raise RuntimeError("Could not create solver")

# Parameters
# Costs C[i][j] for i in 0..3 (factories A1..A4), j in 0..3 (locations B1..B4)
C = [
    [2, 9, 3, 4],
    [8, 3, 5, 7],
    [7, 6, 1, 2],
    [4, 5, 2, 5]
]

# Capacities S[i]
S = [400, 600, 200, 200]

# Demands D[j]
D = [350, 400, 300, 150]

# Fixed costs for new factories (index 2 and 3 correspond to A3 and A4)
F = [0, 0, 1200, 1500]

I = range(4)
J = range(4)

# Decision variables
# x[i][j]: flow from factory i to location j
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

# y[i]: binary variable for building factory i (only for i=2,3 i.e. A3, A4)
y = dict()
for i in [2, 3]:
    y[i] = solver.BoolVar('y_' + str(i))

# Objective function
obj = F[2] * y[2] + F[3] * y[3]
for i in I:
    for j in J:
        obj += C[i][j] * x[i, j]

solver.Minimize(obj)

# Demand satisfaction constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

# Supply capacity constraints
# For existing factories (i=0,1): sum_j x[i][j] <= S[i]
for i in [0, 1]:
    solver.Add(sum(x[i, j] for j in J) <= S[i])

# For new factories (i=2,3): sum_j x[i][j] <= S[i] * y[i]
for i in [2, 3]:
    solver.Add(sum(x[i, j] for j in J) <= S[i] * y[i])

# Exclusive construction constraint: y[2] + y[3] = 1
solver.Add(y[2] + y[3] == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")