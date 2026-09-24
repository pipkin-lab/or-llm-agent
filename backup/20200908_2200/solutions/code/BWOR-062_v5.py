from ortools.linear_solver import pywraplp

# Index sets
I = [1, 2, 3]
J = [0, 1, 2, 3, 4]
N = 4

# Profit data p[i][j]
p = {
    1: {0: 0, 1: 16, 2: 25, 3: 30, 4: 32},
    2: {0: 0, 1: 12, 2: 17, 3: 21, 4: 22},
    3: {0: 0, 1: 10, 2: 14, 3: 16, 4: 17}
}

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    print("Could not create solver")
    exit(1)

# Decision variables: x[i][j] = 1 if region i is assigned exactly j outlets
x = {}
for i in I:
    for j in J:
        x[i, j] = solver.IntVar(0, 1, 'x_{}_{}'.format(i, j))

# Constraint 1: Exactly one allocation level per region
for i in I:
    solver.Add(sum(x[i, j] for j in J) == 1)

# Constraint 2: Total outlets assigned equals N
total_outlets = sum(j * x[i, j] for i in I for j in J)
solver.Add(total_outlets == N)

# Objective: Maximize total profit
objective = sum(p[i][j] * x[i, j] for i in I for j in J)
solver.Maximize(objective)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")