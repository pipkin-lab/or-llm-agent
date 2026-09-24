from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
J = ['A', 'B', 'C']
K = [1, 2, 3, 4]

# Benefit parameters B[j][k]
B = dict()
B['A'] = dict()
B['A'][1] = 41
B['A'][2] = 48
B['A'][3] = 60
B['A'][4] = 66
B['B'] = dict()
B['B'][1] = 42
B['B'][2] = 50
B['B'][3] = 60
B['B'][4] = 66
B['C'] = dict()
B['C'][1] = 64
B['C'][2] = 68
B['C'][3] = 78
B['C'][4] = 76

# Total capital
M = 4

# Decision variables x[j, k] binary
x = dict()
for j in J:
    for k in K:
        x[j, k] = solver.BoolVar('x_' + j + '_' + str(k))

# Objective: maximize total benefit
obj = 0
for j in J:
    for k in K:
        obj += B[j][k] * x[j, k]
solver.Maximize(obj)

# Constraint 1: at most one investment level per project
for j in J:
    solver.Add(sum(x[j, k] for k in K) <= 1)

# Constraint 2: total capital constraint
cap_expr = 0
for j in J:
    for k in K:
        cap_expr += k * x[j, k]
solver.Add(cap_expr <= M)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")