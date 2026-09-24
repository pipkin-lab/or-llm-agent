from ortools.linear_solver import pywraplp

# Define index sets
W = [1, 2, 3, 4]
K = [2, 3, 4]
U_total = 12

# Parameters: A[w][k] = expected accidents for warehouse w with k units
A = dict()
A[(1, 2)] = 18
A[(1, 3)] = 16
A[(1, 4)] = 12
A[(2, 2)] = 38
A[(2, 3)] = 36
A[(2, 4)] = 30
A[(3, 2)] = 14
A[(3, 3)] = 12
A[(3, 4)] = 11
A[(4, 2)] = 34
A[(4, 3)] = 31
A[(4, 4)] = 25

# Create MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x[w, k] is binary
x = dict()
for w in W:
    for k in K:
        x[w, k] = solver.BoolVar('x_' + str(w) + '_' + str(k))

# Objective: minimize total expected accidents
obj_terms = []
for w in W:
    for k in K:
        obj_terms.append(A[(w, k)] * x[w, k])
solver.Minimize(sum(obj_terms))

# Constraint 1: Each warehouse assigned exactly one level
for w in W:
    solver.Add(sum(x[w, k] for k in K) == 1)

# Constraint 2: Total patrol units equal 12
solver.Add(sum(k * x[w, k] for w in W for k in K) == U_total)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")