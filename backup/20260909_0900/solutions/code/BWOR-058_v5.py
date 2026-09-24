from ortools.linear_solver import pywraplp

# Define the solver (MILP since variables are binary)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
A_total = 5000

# Areas per store type
a = {1: 250, 2: 350, 3: 800, 4: 400, 5: 500}

# Min and Max stores per type
L = {1: 1, 2: 1, 3: 1, 4: 0, 5: 1}
U = {1: 3, 2: 2, 3: 3, 4: 2, 5: 3}

# Profit per store p[i][k]
p = {
    1: {1: 9, 2: 8, 3: 7},
    2: {1: 10, 2: 9},
    3: {1: 27, 2: 21, 3: 20},
    4: {1: 16, 2: 10},
    5: {1: 17, 2: 15, 3: 12}
}

r = 0.20

# Decision variables x[i][k]
x = dict()
store_types = [1, 2, 3, 4, 5]

for i in store_types:
    for k in range(L[i], U[i] + 1):
        # Name the variable
        var_name = 'x_' + str(i) + '_' + str(k)
        x[i, k] = solver.BoolVar(var_name)

# Objective function
obj_terms = []
for i in store_types:
    for k in range(L[i], U[i] + 1):
        if k == 0:
            coeff = 0.0
        else:
            coeff = r * k * p[i][k]
        obj_terms.append(coeff * x[i, k])

solver.Maximize(sum(obj_terms))

# Exclusivity constraints: sum_k x[i][k] = 1 for each i
for i in store_types:
    solver.Add(sum(x[i, k] for k in range(L[i], U[i] + 1)) == 1)

# Area constraint
area_terms = []
for i in store_types:
    for k in range(L[i], U[i] + 1):
        area_terms.append(a[i] * k * x[i, k])

solver.Add(sum(area_terms) <= A_total)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")