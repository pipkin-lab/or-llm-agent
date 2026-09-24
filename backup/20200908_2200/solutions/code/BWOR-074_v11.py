from ortools.linear_solver import pywraplp

# Define the problem parameters
grades = ['A', 'B', 'C', 'D', 'E']
counts = dict()
counts['A'] = 5000
counts['B'] = 12500
counts['C'] = 15000
counts['D'] = 10000
counts['E'] = 7500

num_grades = len(grades)
positions = range(1, num_grades + 1)  # Positions 1 to 5

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x[g, p] is 1 if grade g is assigned to position p
x = dict()
for g in grades:
    for p in positions:
        x[g, p] = solver.IntVar(0, 1, 'x_' + g + '_' + str(p))

# Constraints
# 1. Each grade is assigned to exactly one position
for g in grades:
    solver.Add(sum(x[g, p] for p in positions) == 1)

# 2. Each position is occupied by exactly one grade
for p in positions:
    solver.Add(sum(x[g, p] for g in grades) == 1)

# Objective function: Minimize total workload
# Z = sum over g, p of n_g * (p - 1) * x[g, p]
objective = 0
for g in grades:
    for p in positions:
        objective += counts[g] * (p - 1) * x[g, p]

solver.Minimize(objective)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")