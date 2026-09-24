from ortools.linear_solver import pywraplp

# Define the problem parameters
# Set of Grades
grades = ['A', 'B', 'C', 'D', 'E']

# Set of Positions (1 to 5)
positions = range(1, 6)

# Number of sheets for each grade
N = {
    'A': 5000,
    'B': 12500,
    'C': 15000,
    'D': 10000,
    'E': 7500
}

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Create decision variables
# x[g, p] is a binary variable indicating if grade g is sorted at position p
x = dict()
for g in grades:
    for p in positions:
        x[g, p] = solver.IntVar(0, 1, 'x_' + g + '_' + str(p))

# Objective Function
# Minimize Z = sum(g in G, p in P) p * N_g * x[g, p]
obj_terms = []
for g in grades:
    for p in positions:
        obj_terms.append(p * N[g] * x[g, p])

solver.Minimize(sum(obj_terms))

# Constraints
# 1. Each grade is assigned to exactly one position
for g in grades:
    solver.Add(sum(x[g, p] for p in positions) == 1)

# 2. Each position is assigned exactly one grade
for p in positions:
    solver.Add(sum(x[g, p] for g in grades) == 1)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")