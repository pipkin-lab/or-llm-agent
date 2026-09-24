from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index set
R = [1, 2, 3, 4]

# Parameters
f = dict()
f[1] = 3
f[2] = 2
f[3] = 1
f[4] = 1

S = dict()
S[1] = 36
S[2] = 8
S[3] = 16
S[4] = 28

# Decision variables
x = dict()
for r in R:
    x[r] = solver.IntVar(0, solver.infinity(), 'x_' + str(r))

# Objective: minimize total ships
obj = 0
for r in R:
    obj = obj + x[r]
solver.Minimize(obj)

# Constraints: x_r >= f_r * S_r
for r in R:
    solver.Add(x[r] >= f[r] * S[r])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")