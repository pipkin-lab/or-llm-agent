from ortools.linear_solver import pywraplp

# Parameter definitions based on the mathematical model
J = ['A', 'B', 'C']
K = [0, 1, 2, 3, 4]
C_total = 4

# Benefit parameters b[j][k]
b = dict()
b['A'] = dict()
b['A'][0] = 0
b['A'][1] = 41
b['A'][2] = 48
b['A'][3] = 60
b['A'][4] = 66

b['B'] = dict()
b['B'][0] = 0
b['B'][1] = 42
b['B'][2] = 50
b['B'][3] = 60
b['B'][4] = 66

b['C'] = dict()
b['C'][0] = 0
b['C'][1] = 64
b['C'][2] = 68
b['C'][3] = 78
b['C'][4] = 76

# Investment amount x[j][k] = k
x = dict()
for j in J:
    x[j] = dict()
    for k in K:
        x[j][k] = k

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables y[j][k]
y = dict()
for j in J:
    y[j] = dict()
    for k in K:
        y[j][k] = solver.BoolVar('y_' + j + '_' + str(k))

# Objective function: Maximize total benefit
obj_terms = []
for j in J:
    for k in K:
        obj_terms.append(b[j][k] * y[j][k])
solver.Maximize(sum(obj_terms))

# Constraint 1: Single selection (exactly one level per project)
for j in J:
    level_terms = []
    for k in K:
        level_terms.append(y[j][k])
    solver.Add(sum(level_terms) == 1)

# Constraint 2: Capital constraint
cost_terms = []
for j in J:
    for k in K:
        cost_terms.append(x[j][k] * y[j][k])
solver.Add(sum(cost_terms) <= C_total)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")