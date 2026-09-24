from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
n = 4
cities = [1, 2, 3, 4]
s = 1

# Cost matrix c[i][j]
c = dict()
c[1, 2] = 6
c[1, 3] = 7
c[1, 4] = 9
c[2, 1] = 8
c[2, 3] = 9
c[2, 4] = 7
c[3, 1] = 5
c[3, 2] = 8
c[3, 4] = 8
c[4, 1] = 6
c[4, 2] = 5
c[4, 3] = 5

# Binary variables x[i, j] for all i != j
x = dict()
for i in cities:
    for j in cities:
        if i != j:
            x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Continuous auxiliary variables u[i] for i != s
u = dict()
for i in cities:
    if i != s:
        u[i] = solver.NumVar(0, n - 1, 'u_' + str(i))

# Objective: minimize total distance
obj = 0
for i in cities:
    for j in cities:
        if i != j:
            obj += c[i, j] * x[i, j]
solver.Minimize(obj)

# Flow balance constraints
for i in cities:
    # Outgoing: exactly one arc leaves city i
    out_expr = sum(x[i, j] for j in cities if j != i)
    solver.Add(out_expr == 1)
    # Incoming: exactly one arc enters city i
    in_expr = sum(x[j, i] for j in cities if j != i)
    solver.Add(in_expr == 1)

# MTZ subtour elimination constraints: u[i] - u[j] + n * x[i, j] <= n - 1
# Applied for i, j in V \ {s}, i != j
non_start_cities = [i for i in cities if i != s]
for i in non_start_cities:
    for j in non_start_cities:
        if i != j:
            solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)

# Fix u[s] = 0 (implicitly, since u is only defined for i != s, and MTZ uses u[i] - u[j]
# where both are in non_start. But we need to ensure consistency.
# Actually, the standard MTZ constraint is u[i] - u[j] + n*x[i,j] <= n-1 for all i,j != s.
# And u[s] = 0 is fixed. Since u[s] is not a variable, we just need to make sure
# the constraints are consistent. In this formulation, u[s] is not a variable,
# so the constraints only involve u[i] and u[j] for i,j != s.
# This is correct.

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")