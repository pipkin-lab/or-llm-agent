from ortools.linear_solver import pywraplp

# Initialize MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
W = [1, 2, 3, 4]
U = [2, 3, 4]

# Parameters: a[w][u] = expected accidents for warehouse w with u patrol units
a = dict()
a[(1, 2)] = 18
a[(1, 3)] = 16
a[(1, 4)] = 12
a[(2, 2)] = 38
a[(2, 3)] = 36
a[(2, 4)] = 30
a[(3, 2)] = 14
a[(3, 3)] = 12
a[(3, 4)] = 11
a[(4, 2)] = 34
a[(4, 3)] = 31
a[(4, 4)] = 25

P = 12

# Decision variables: x[w, u] = 1 if warehouse w is assigned u patrol units
x = dict()
for w in W:
    for u in U:
        x[w, u] = solver.BoolVar('x_{}_{}'.format(w, u))

# Objective: minimize total expected accidents
obj_terms = []
for w in W:
    for u in U:
        obj_terms.append(a[(w, u)] * x[w, u])
solver.Minimize(sum(obj_terms))

# Constraint 1: Each warehouse is assigned exactly one patrol-unit level
for w in W:
    solver.Add(sum(x[w, u] for u in U) == 1)

# Constraint 2: Total patrol units used equals available supply
total_units_expr = 0
for w in W:
    for u in U:
        total_units_expr += u * x[w, u]
solver.Add(total_units_expr == P)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")