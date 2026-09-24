from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x[t, k] for t in {1,2,3}, k in {1,2}
x = dict()
for t in [1, 2, 3]:
    for k in [1, 2]:
        x[t, k] = solver.IntVar(0, INF, 'x_%d_%d' % (t, k))

# Objective function coefficients
# Z = 100*x[1,1] + 260*x[1,2] + 100*x[2,1] + 80*x[2,2] + 400*x[3,1] + 340*x[3,2]
objective = (100 * x[1, 1] + 260 * x[1, 2] + 100 * x[2, 1]
             + 80 * x[2, 2] + 400 * x[3, 1] + 340 * x[3, 2])
solver.Minimize(objective)

# Constraint 1: 42*x[1,1] + 114*x[1,2] >= 10000
solver.Add(42 * x[1, 1] + 114 * x[1, 2] >= 10000)

# Constraint 2: 42*x[2,1] + 36*x[2,2] >= 20000
solver.Add(42 * x[2, 1] + 36 * x[2, 2] >= 20000)

# Constraint 3: 180*x[3,1] + 150*x[3,2] >= 30000
solver.Add(180 * x[3, 1] + 150 * x[3, 2] >= 30000)

# Constraint 4: x[1,1] + x[1,2] + x[2,1] + x[3,2] <= 400
solver.Add(x[1, 1] + x[1, 2] + x[2, 1] + x[3, 2] <= 400)

# Constraint 5: 2*x[1,2] + x[2,2] + 5*x[3,1] + 3*x[3,2] <= 800
solver.Add(2 * x[1, 2] + x[2, 2] + 5 * x[3, 1] + 3 * x[3, 2] <= 800)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")