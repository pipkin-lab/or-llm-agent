from ortools.linear_solver import pywraplp

# Parameters
I = [1, 2, 3, 4, 5, 6]
J = [1, 2, 3, 4, 5, 6]

D = dict()
D[1] = 500
D[2] = 550
D[3] = 700
D[4] = 900
D[5] = 400
D[6] = 300

C = dict()
C[1] = 5
C[2] = 8
C[3] = 10
C[4] = 12
C[5] = 16
C[6] = 18

F = dict()
F[1] = 1200
F[2] = 1200
F[3] = 1200
F[4] = 1200
F[5] = 1200
F[6] = 1200

Cap = dict()
Cap[1] = 1500
Cap[2] = 2500
Cap[3] = 4000
Cap[4] = 6000
Cap[5] = 9000
Cap[6] = 12000

# Valid substitution pairs: (i, j) where Cap[j] >= Cap[i]
valid_pairs = dict()
for i in I:
    valid_pairs[i] = [j for j in J if Cap[j] >= Cap[i]]

# Big-M values: M_j = sum of D_i for all i where (i,j) is valid
M = dict()
for j in J:
    M[j] = 0
    for i in I:
        if Cap[j] >= Cap[i]:
            M[j] += D[i]

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for i in I:
    for j in valid_pairs[i]:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

y = dict()
for j in J:
    y[j] = solver.BoolVar('y_' + str(j))

# Objective function
obj_terms = []
for j in J:
    obj_terms.append(F[j] * y[j])
    for i in I:
        if (i, j) in x:
            obj_terms.append(C[j] * x[i, j])

objective = sum(obj_terms)
solver.Minimize(objective)

# Demand satisfaction constraints
for i in I:
    demand_expr = sum(x[i, j] for j in valid_pairs[i])
    solver.Add(demand_expr == D[i])

# Machine activation constraints (fixed-charge logic)
for j in J:
    prod_expr = sum(x[i, j] for i in I if (i, j) in x)
    solver.Add(prod_expr <= M[j] * y[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")