from ortools.linear_solver import pywraplp

# Define the problem parameters
G = ['A', 'B', 'C', 'D', 'E']
P = [1, 2, 3, 4, 5]

C = {
    'A': 5000,
    'B': 12500,
    'C': 15000,
    'D': 10000,
    'E': 7500
}

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    print("Could not create solver")
    exit(1)

# Decision variables
# x[g, k] = 1 if grade g is scanned at position k
x = dict()
for g in G:
    for k in P:
        x[g, k] = solver.IntVar(0, 1, 'x_' + g + '_' + str(k))

# Constraints
# 1. Each grade is assigned to exactly one position
for g in G:
    solver.Add(sum(x[g, k] for k in P) == 1)

# 2. Each position is assigned exactly one grade
for k in P:
    solver.Add(sum(x[g, k] for g in G) == 1)

# Objective Function: Minimize Z = sum(C_g * k * x[g, k])
obj_terms = []
for g in G:
    for k in P:
        obj_terms.append(C[g] * k * x[g, k])

solver.Minimize(sum(obj_terms))

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")