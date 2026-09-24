from ortools.linear_solver import pywraplp

# Initialize the solver (LP problem, use GLOP)
solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    print("No solver available.")
    exit(1)

# Index sets
I = [1, 2, 3]
J = [1, 2, 3]

# Parameters
a = {1: 20, 2: 30, 3: 20}  # Supply capacity of mills
b = {1: 15, 2: 25, 3: 20}  # Demand of factories
c = {
    (1, 1): 3, (1, 2): 10, (1, 3): 2,
    (2, 1): 4, (2, 2): 11, (2, 3): 8,
    (3, 1): 8, (3, 2): 11, (3, 3): 4
}
p = {1: 12, 2: 16, 3: 11}  # Unit profit at factories

# Net unit benefit r_ij = p_j - c_ij
r = dict()
for i in I:
    for j in J:
        r[i, j] = p[j] - c[i, j]

# Decision variables x[i, j] >= 0
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

# Objective: Maximize sum r[i,j] * x[i,j]
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(r[i, j] * x[i, j])
solver.Maximize(sum(obj_terms))

# Supply constraints: sum_j x[i,j] <= a[i]
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= a[i])

# Demand constraints: sum_i x[i,j] = b[j]
for j in J:
    solver.Add(sum(x[i, j] for i in I) == b[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")