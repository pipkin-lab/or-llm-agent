from ortools.linear_solver import pywraplp

# Index sets
P = ['A', 'B', 'C']
K = [0, 1, 2, 3, 4]

# Benefit table B[p][k]
B = dict()
B['A'] = dict()
B['A'][0] = 0
B['A'][1] = 41
B['A'][2] = 48
B['A'][3] = 60
B['A'][4] = 66

B['B'] = dict()
B['B'][0] = 0
B['B'][1] = 42
B['B'][2] = 50
B['B'][3] = 60
B['B'][4] = 66

B['C'] = dict()
B['C'][0] = 0
B['C'][1] = 64
B['C'][2] = 68
B['C'][3] = 78
B['C'][4] = 76

C_total = 4

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables y[p][k]
y = dict()
for p in P:
    y[p] = dict()
    for k in K:
        y[p][k] = solver.BoolVar('y_' + p + '_' + str(k))

# Constraint 1: Exactly one investment level per project
for p in P:
    solver.Add(sum(y[p][k] for k in K) == 1)

# Constraint 2: Total capital constraint
solver.Add(sum(k * y[p][k] for p in P for k in K) <= C_total)

# Objective: Maximize total benefit
obj = sum(B[p][k] * y[p][k] for p in P for k in K)
solver.Maximize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")