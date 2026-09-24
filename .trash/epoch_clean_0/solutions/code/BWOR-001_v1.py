from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
x = dict()
R = ['A', 'B', 'C']
P = ['X', 'Y', 'Z']

for r in R:
    for p in P:
        x[r, p] = solver.NumVar(0, solver.infinity(), 'x_' + r + '_' + p)

# Objective function
obj = 0.90 * x['A', 'X'] + 1.40 * x['B', 'X'] + 1.90 * x['C', 'X']
obj += 0.45 * x['A', 'Y'] + 0.95 * x['B', 'Y'] + 1.45 * x['C', 'Y']
obj += -0.05 * x['A', 'Z'] + 0.45 * x['B', 'Z'] + 0.95 * x['C', 'Z']

solver.Maximize(obj)

# Material Supply Constraints
solver.Add(x['A', 'X'] + x['A', 'Y'] + x['A', 'Z'] <= 2000)
solver.Add(x['B', 'X'] + x['B', 'Y'] + x['B', 'Z'] <= 2500)
solver.Add(x['C', 'X'] + x['C', 'Y'] + x['C', 'Z'] <= 1200)

# Composition Constraints

# Brand X: A >= 60%
solver.Add(2 * x['A', 'X'] - 3 * x['B', 'X'] - 3 * x['C', 'X'] >= 0)

# Brand X: C <= 20%
solver.Add(x['C', 'X'] - 0.25 * x['A', 'X'] - 0.25 * x['B', 'X'] <= 0)

# Brand Y: A >= 30%
solver.Add(7 * x['A', 'Y'] - 3 * x['B', 'Y'] - 3 * x['C', 'Y'] >= 0)

# Brand Y: C <= 50%
solver.Add(x['C', 'Y'] - x['A', 'Y'] - x['B', 'Y'] <= 0)

# Brand Z: C <= 60%
solver.Add(2 * x['C', 'Z'] - 3 * x['A', 'Z'] - 3 * x['B', 'Z'] <= 0)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")