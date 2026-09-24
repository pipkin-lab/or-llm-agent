from ortools.linear_solver import pywraplp

# Data
feeds = [1, 2, 3, 4, 5]
nutrients = ['P', 'M', 'V']

# Nutrient content per kg of feed (a[n][f])
a = {
    'P': [3, 2, 1, 6, 18],
    'M': [1.0, 0.5, 0.2, 2.0, 0.5],
    'V': [0.5, 1.0, 0.2, 2.0, 0.8]
}

# Cost per kg of feed (c[f])
c = [0.2, 0.7, 0.4, 0.3, 0.8]

# Minimum daily requirements (R[n])
R = {'P': 700, 'M': 30, 'V': 100}

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables: x[f] >= 0 for each feed f
x = dict()
for i in range(len(feeds)):
    x[i] = solver.NumVar(0, solver.infinity(), 'x_' + str(feeds[i]))

# Objective function: minimize total cost
objective = 0
for i in range(len(feeds)):
    objective += c[i] * x[i]
solver.Minimize(objective)

# Nutritional constraints
# Protein constraint
protein_expr = 0
for i in range(len(feeds)):
    protein_expr += a['P'][i] * x[i]
solver.Add(protein_expr >= R['P'])

# Minerals constraint
minerals_expr = 0
for i in range(len(feeds)):
    minerals_expr += a['M'][i] * x[i]
solver.Add(minerals_expr >= R['M'])

# Vitamins constraint
vitamins_expr = 0
for i in range(len(feeds)):
    vitamins_expr += a['V'][i] * x[i]
solver.Add(vitamins_expr >= R['V'])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")