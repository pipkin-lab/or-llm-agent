from ortools.linear_solver import pywraplp

# Initialize solver (MILP because of binary variables)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
I = [1, 2, 3]  # spare part types
K = [1, 2, 3]  # discrete levels

# Parameters
B = 8  # Budget limit in thousand yuan

r = {
    (1, 1): 0.3, (1, 2): 0.4, (1, 3): 0.5,
    (2, 1): 0.2, (2, 2): 0.5, (2, 3): 0.9,
    (3, 1): 0.1, (3, 2): 0.2, (3, 3): 0.7
}

c = {
    (1, 1): 1, (1, 2): 2, (1, 3): 3,
    (2, 1): 3, (2, 2): 5, (2, 3): 6,
    (3, 1): 2, (3, 2): 3, (3, 3): 4
}

# Decision variables: x[i, k] binary
x = dict()
for i in I:
    for k in K:
        x[i, k] = solver.BoolVar('x_{}_{}'.format(i, k))

# Objective function: Maximize total reliability increase
obj = sum(r[i, k] * x[i, k] for i in I for k in K)
solver.Maximize(obj)

# Constraint 1: Exactly one level selected for each part type
for i in I:
    solver.Add(sum(x[i, k] for k in K) == 1)

# Constraint 2: Budget constraint
solver.Add(sum(c[i, k] * x[i, k] for i in I for k in K) <= B)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")