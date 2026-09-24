from ortools.linear_solver import pywraplp

# Create the LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
# x[k][m] where k in {0,1,2} for products I, II, III and m in {'A1','A2','B1','B2','B3'}
x = dict()

# Stage A variables
x[0, 'A1'] = solver.NumVar(0, solver.infinity(), 'x_0_A1')
x[0, 'A2'] = solver.NumVar(0, solver.infinity(), 'x_0_A2')
x[1, 'A1'] = solver.NumVar(0, solver.infinity(), 'x_1_A1')
x[1, 'A2'] = solver.NumVar(0, solver.infinity(), 'x_1_A2')
x[2, 'A2'] = solver.NumVar(0, solver.infinity(), 'x_2_A2')

# Stage B variables
x[0, 'B1'] = solver.NumVar(0, solver.infinity(), 'x_0_B1')
x[0, 'B2'] = solver.NumVar(0, solver.infinity(), 'x_0_B2')
x[0, 'B3'] = solver.NumVar(0, solver.infinity(), 'x_0_B3')
x[1, 'B2'] = solver.NumVar(0, solver.infinity(), 'x_1_B2')
x[2, 'B2'] = solver.NumVar(0, solver.infinity(), 'x_2_B2')

# Objective function coefficients
# Profit = (p_k - r_k) * Q_k - sum of processing costs
# Q_0 = x[0,'A1'] + x[0,'A2']
# Q_1 = x[1,'A1'] + x[1,'A2']
# Q_2 = x[2,'A2']

# Contribution margins
margin_0 = 1.00
margin_1 = 1.65
margin_2 = 2.30

# Processing costs
# A1: 0.05 * (5*x[0,'A1'] + 10*x[1,'A1'])
# A2: 0.03 * (7*x[0,'A2'] + 9*x[1,'A2'] + 12*x[2,'A2'])
# B1: 0.06 * (6*x[0,'B1'])
# B2: 0.11 * (4*x[0,'B2'] + 8*x[1,'B2'] + 11*x[2,'B2'])
# B3: 0.05 * (7*x[0,'B3'])

objective_terms = []

# Add margin terms
objective_terms.append(margin_0 * x[0, 'A1'])
objective_terms.append(margin_0 * x[0, 'A2'])
objective_terms.append(margin_1 * x[1, 'A1'])
objective_terms.append(margin_1 * x[1, 'A2'])
objective_terms.append(margin_2 * x[2, 'A2'])

# Subtract processing costs
objective_terms.append(-0.05 * 5 * x[0, 'A1'])
objective_terms.append(-0.05 * 10 * x[1, 'A1'])
objective_terms.append(-0.03 * 7 * x[0, 'A2'])
objective_terms.append(-0.03 * 9 * x[1, 'A2'])
objective_terms.append(-0.03 * 12 * x[2, 'A2'])
objective_terms.append(-0.06 * 6 * x[0, 'B1'])
objective_terms.append(-0.11 * 4 * x[0, 'B2'])
objective_terms.append(-0.11 * 8 * x[1, 'B2'])
objective_terms.append(-0.11 * 11 * x[2, 'B2'])
objective_terms.append(-0.05 * 7 * x[0, 'B3'])

solver.Maximize(sum(objective_terms))

# Constraints

# Flow conservation
# Product 0 (I)
solver.Add(x[0, 'A1'] + x[0, 'A2'] == x[0, 'B1'] + x[0, 'B2'] + x[0, 'B3'])
# Product 1 (II)
solver.Add(x[1, 'A1'] + x[1, 'A2'] == x[1, 'B2'])
# Product 2 (III)
solver.Add(x[2, 'A2'] == x[2, 'B2'])

# Machine capacities
# A1: 6000 hours
solver.Add(5 * x[0, 'A1'] + 10 * x[1, 'A1'] <= 6000)
# A2: 10000 hours
solver.Add(7 * x[0, 'A2'] + 9 * x[1, 'A2'] + 12 * x[2, 'A2'] <= 10000)
# B1: 4000 hours
solver.Add(6 * x[0, 'B1'] <= 4000)
# B2: 7000 hours
solver.Add(4 * x[0, 'B2'] + 8 * x[1, 'B2'] + 11 * x[2, 'B2'] <= 7000)
# B3: 4000 hours
solver.Add(7 * x[0, 'B3'] <= 4000)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")