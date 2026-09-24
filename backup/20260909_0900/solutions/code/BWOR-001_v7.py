from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Define the raw materials and brands
materials = ['A', 'B', 'C']
brands = ['X', 'Y', 'Z']

# Decision variables: x[i][j] for i in materials, j in brands
x = dict()
for i in materials:
    for j in brands:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + i + '_' + j)

# Objective function coefficients: p_j - q_j - c_i
# p = [3.40, 2.85, 2.25]
# q = [0.50, 0.40, 0.30]
# c = [2.00, 1.50, 1.00]
# Coeff[i, j] = p_j - q_j - c_i

# Brand X (j=0)
# A: 3.40 - 0.50 - 2.00 = 0.90
# B: 3.40 - 0.50 - 1.50 = 1.40
# C: 3.40 - 0.50 - 1.00 = 1.90
# Brand Y (j=1)
# A: 2.85 - 0.40 - 2.00 = 0.45
# B: 2.85 - 0.40 - 1.50 = 0.95
# C: 2.85 - 0.40 - 1.00 = 1.45
# Brand Z (j=2)
# A: 2.25 - 0.30 - 2.00 = -0.05
# B: 2.25 - 0.30 - 1.50 = 0.45
# C: 2.25 - 0.30 - 1.00 = 0.95

obj_terms = []
obj_terms.append(0.90 * x['A', 'X'])
obj_terms.append(1.40 * x['B', 'X'])
obj_terms.append(1.90 * x['C', 'X'])
obj_terms.append(0.45 * x['A', 'Y'])
obj_terms.append(0.95 * x['B', 'Y'])
obj_terms.append(1.45 * x['C', 'Y'])
obj_terms.append(-0.05 * x['A', 'Z'])
obj_terms.append(0.45 * x['B', 'Z'])
obj_terms.append(0.95 * x['C', 'Z'])

solver.Maximize(sum(obj_terms))

# Material Availability Constraints
# 1. Material A: x_AX + x_AY + x_AZ <= 2000
solver.Add(x['A', 'X'] + x['A', 'Y'] + x['A', 'Z'] <= 2000)

# 2. Material B: x_BX + x_BY + x_BZ <= 2500
solver.Add(x['B', 'X'] + x['B', 'Y'] + x['B', 'Z'] <= 2500)

# 3. Material C: x_CX + x_CY + x_CZ <= 1200
solver.Add(x['C', 'X'] + x['C', 'Y'] + x['C', 'Z'] <= 1200)

# Composition Constraints
# Brand X:
# 4. A >= 60% => 0.40 x_AX - 0.60 x_BX - 0.60 x_CX >= 0
solver.Add(0.40 * x['A', 'X'] - 0.60 * x['B', 'X'] - 0.60 * x['C', 'X'] >= 0)
# 5. C <= 20% => -0.20 x_AX - 0.20 x_BX + 0.80 x_CX <= 0
solver.Add(-0.20 * x['A', 'X'] - 0.20 * x['B', 'X'] + 0.80 * x['C', 'X'] <= 0)

# Brand Y:
# 6. A >= 30% => 0.70 x_AY - 0.30 x_BY - 0.30 x_CY >= 0
solver.Add(0.70 * x['A', 'Y'] - 0.30 * x['B', 'Y'] - 0.30 * x['C', 'Y'] >= 0)
# 7. C <= 50% => -0.50 x_AY - 0.50 x_BY + 0.50 x_CY <= 0
solver.Add(-0.50 * x['A', 'Y'] - 0.50 * x['B', 'Y'] + 0.50 * x['C', 'Y'] <= 0)

# Brand Z:
# 8. C <= 60% => -0.60 x_AZ - 0.60 x_BZ + 0.40 x_CZ <= 0
solver.Add(-0.60 * x['A', 'Z'] - 0.60 * x['B', 'Z'] + 0.40 * x['C', 'Z'] <= 0)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")