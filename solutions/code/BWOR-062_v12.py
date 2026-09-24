from ortools.linear_solver import pywraplp

# Parameters
R = [1, 2, 3]
K = [0, 1, 2, 3, 4]
N = 4

p = dict()
p[1, 0] = 0
p[1, 1] = 16
p[1, 2] = 25
p[1, 3] = 30
p[1, 4] = 32
p[2, 0] = 0
p[2, 1] = 12
p[2, 2] = 17
p[2, 3] = 21
p[2, 4] = 22
p[3, 0] = 0
p[3, 1] = 10
p[3, 2] = 14
p[3, 3] = 16
p[3, 4] = 17

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: binary x[r, k]
x = dict()
for r in R:
    for k in K:
        x[r, k] = solver.BoolVar('x_{}_{}'.format(r, k))

# Objective
obj = sum(p[r, k] * x[r, k] for r in R for k in K)
solver.Maximize(obj)

# Constraint 1: exactly one outlet count per region
for r in R:
    solver.Add(sum(x[r, k] for k in K) == 1)

# Constraint 2: total outlets allocated equals N
solver.Add(sum(k * x[r, k] for r in R for k in K) == N)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")