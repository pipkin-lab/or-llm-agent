from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Time periods
T = [1, 2, 3, 4, 5, 6]

# Demand (in hundreds of units)
d = dict()
d[1] = 1
d[2] = 2
d[3] = 5
d[4] = 3
d[5] = 2
d[6] = 1

# Decision variables
x = dict()
I = dict()
y = dict()

for t in T:
    x[t] = solver.NumVar(0, 4, 'x_' + str(t))
    I[t] = solver.NumVar(0, 3, 'I_' + str(t))
    y[t] = solver.BoolVar('y_' + str(t))

# Inventory balance constraints
for t in T:
    if t == 1:
        solver.Add(I[t] == x[t] - d[t])
    else:
        solver.Add(I[t] == I[t - 1] + x[t] - d[t])

# Final inventory must be 0
solver.Add(I[6] == 0)

# Linking constraints: x_t <= 4 * y_t
for t in T:
    solver.Add(x[t] <= 4 * y[t])

# Objective function
obj = 0
for t in T:
    obj += 10000 * x[t]
    obj += 4000 * y[t]

for t in [1, 2, 3, 4, 5]:
    obj += 1000 * I[t]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")