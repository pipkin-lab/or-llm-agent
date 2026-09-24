from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

toys = ['A', 'B', 'C']
stores = ['X', 'Y', 'Z']

# Create decision variables
x = dict()
for i in toys:
    for j in stores:
        x[i, j] = solver.IntVar(0, solver.infinity(), 'x_' + i + '_' + j)

# Profit coefficients
profit = dict()
profit['A', 'X'] = 5
profit['A', 'Y'] = 4
profit['A', 'Z'] = 0
profit['B', 'X'] = 16
profit['B', 'Y'] = 8
profit['B', 'Z'] = 6
profit['C', 'X'] = 12
profit['C', 'Y'] = 10
profit['C', 'Z'] = 11

# Objective function
obj = 0
for i in toys:
    for j in stores:
        obj += profit[i, j] * x[i, j]

solver.Maximize(obj)

# Supply constraints
solver.Add(x['A', 'X'] + x['A', 'Y'] + x['A', 'Z'] <= 1000)
solver.Add(x['B', 'X'] + x['B', 'Y'] + x['B', 'Z'] <= 2000)
solver.Add(x['C', 'X'] + x['C', 'Y'] + x['C', 'Z'] <= 2000)

# Demand capacity constraints (per store per toy <= 1500)
for i in toys:
    for j in stores:
        solver.Add(x[i, j] <= 1500)

# Specific operational constraints
# Store Z requires at least 1000 units of Toy C
solver.Add(x['C', 'Z'] >= 1000)

# Store Z refuses Toy A
solver.Add(x['A', 'Z'] == 0)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")