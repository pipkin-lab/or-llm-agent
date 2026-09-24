from ortools.linear_solver import pywraplp

# Define the solver (GLOP for linear programming)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
F = 5  # Number of feed types
N = 3  # Number of nutrients

# Costs
c = [0.2, 0.7, 0.4, 0.3, 0.8]

# Nutritional coefficients a[f][n] (f: 0..4, n: 0..2)
a = [
    [3, 1.0, 0.5],   # Feed 1
    [2, 0.5, 1.0],   # Feed 2
    [1, 0.2, 0.2],   # Feed 3
    [6, 2.0, 2.0],   # Feed 4
    [18, 0.5, 0.8]   # Feed 5
]

# Minimum nutritional requirements
R = [700, 30, 100]

# Decision variables: x_f >= 0
x = dict()
for f in range(F):
    x[f] = solver.NumVar(0, solver.infinity(), 'x_' + str(f))

# Objective function: minimize total cost
obj = sum(c[f] * x[f] for f in range(F))
solver.Minimize(obj)

# Nutritional constraints
for n in range(N):
    constraint = sum(a[f][n] * x[f] for f in range(F))
    solver.Add(constraint >= R[n])

# Solve the problem
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")