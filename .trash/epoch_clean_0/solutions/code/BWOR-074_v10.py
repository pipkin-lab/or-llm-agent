from ortools.linear_solver import pywraplp

# Initialize the solver for Mixed-Integer Programming
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index Sets
G = ['A', 'B', 'C', 'D', 'E']
N = [1, 2, 3, 4, 5]

# Parameters
V = 50000
p = {'A': 0.10, 'B': 0.25, 'C': 0.30, 'D': 0.20, 'E': 0.15}
n = {}
for g in G:
    n[g] = int(V * p[g])

# Decision Variables
# x[g, k] = 1 if grade g is sorted at position k
x = dict()
for g in G:
    for k in N:
        x[g, k] = solver.BoolVar('x_' + g + '_' + str(k))

# Objective Function
# Minimize Z = sum(n_g * k * x[g, k])
obj_terms = []
for g in G:
    for k in N:
        obj_terms.append(n[g] * k * x[g, k])
solver.Minimize(sum(obj_terms))

# Constraints
# 1. Each grade is assigned to exactly one position
for g in G:
    solver.Add(sum(x[g, k] for k in N) == 1)

# 2. Each position is assigned exactly one grade
for k in N:
    solver.Add(sum(x[g, k] for g in G) == 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")