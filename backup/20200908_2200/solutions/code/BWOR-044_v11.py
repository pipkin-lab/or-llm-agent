from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Index sets
origins = [1, 2, 3]
destinations = ['A', 'B', 'C']

# Parameters
S = {1: 20, 2: 40, 3: 30}
D = {'A': 30, 'B': 20, 'C': 20}
c = {
    (1, 'A'): 1, (1, 'B'): 2, (1, 'C'): 2,
    (2, 'A'): 1, (2, 'B'): 4, (2, 'C'): 5,
    (3, 'A'): 2, (3, 'B'): 3, (3, 'C'): 3
}
h = {1: 5, 2: 4, 3: 3}
L = {1: 0, 2: 38, 3: 27}

# Decision variables
x = dict()
for i in origins:
    for j in destinations:
        x[i, j] = solver.NumVar(0, inf, 'x_' + str(i) + '_' + j)

y = dict()
for i in origins:
    y[i] = solver.NumVar(0, inf, 'y_' + str(i))

# Objective function
obj_terms = []
for i in origins:
    for j in destinations:
        obj_terms.append(c[(i, j)] * x[i, j])
    obj_terms.append(h[i] * y[i])

solver.Minimize(sum(obj_terms))

# Supply constraints
for i in origins:
    constraint = sum(x[i, j] for j in destinations) + y[i] <= S[i]
    solver.Add(constraint)

# Demand constraints
for j in destinations:
    solver.Add(sum(x[i, j] for i in origins) == D[j])

# Minimum shipment constraints
for i in origins:
    if L[i] > 0:
        solver.Add(sum(x[i, j] for j in destinations) >= L[i])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")