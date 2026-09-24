from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Define raw materials and products
raw_materials = ['A', 'B', 'C']
products = ['X', 'Y', 'Z']

# Parameters
c = {'A': 2.00, 'B': 1.50, 'C': 1.00}
M = {'A': 2000, 'B': 2500, 'C': 1200}
p = {'X': 3.40, 'Y': 2.85, 'Z': 2.25}
q = {'X': 0.50, 'Y': 0.40, 'Z': 0.30}

# Decision variables: x[r, j] = amount of raw material r used in product j
x = dict()
for r in raw_materials:
    for j in products:
        x[r, j] = solver.NumVar(0, solver.infinity(), 'x_' + r + '_' + j)

# Objective function: Maximize profit
# Z = sum over r, j of (p_j - q_j - c_r) * x[r, j]
objective = 0
for r in raw_materials:
    for j in products:
        coeff = p[j] - q[j] - c[r]
        objective += coeff * x[r, j]

solver.Maximize(objective)

# Raw Material Supply Constraints
for r in raw_materials:
    solver.Add(sum(x[r, j] for j in products) <= M[r])

# Composition Constraints for Brand X
# A >= 60%: 0.40*x[A,X] - 0.60*x[B,X] - 0.60*x[C,X] >= 0
solver.Add(0.40 * x['A', 'X'] - 0.60 * x['B', 'X'] - 0.60 * x['C', 'X'] >= 0)
# C <= 20%: -0.20*x[A,X] - 0.20*x[B,X] + 0.80*x[C,X] <= 0
solver.Add(-0.20 * x['A', 'X'] - 0.20 * x['B', 'X'] + 0.80 * x['C', 'X'] <= 0)

# Composition Constraints for Brand Y
# A >= 30%: 0.70*x[A,Y] - 0.30*x[B,Y] - 0.30*x[C,Y] >= 0
solver.Add(0.70 * x['A', 'Y'] - 0.30 * x['B', 'Y'] - 0.30 * x['C', 'Y'] >= 0)
# C <= 50%: -0.50*x[A,Y] - 0.50*x[B,Y] + 0.50*x[C,Y] <= 0
solver.Add(-0.50 * x['A', 'Y'] - 0.50 * x['B', 'Y'] + 0.50 * x['C', 'Y'] <= 0)

# Composition Constraints for Brand Z
# C <= 60%: -0.60*x[A,Z] - 0.60*x[B,Z] + 0.40*x[C,Z] <= 0
solver.Add(-0.60 * x['A', 'Z'] - 0.60 * x['B', 'Z'] + 0.40 * x['C', 'Z'] <= 0)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")