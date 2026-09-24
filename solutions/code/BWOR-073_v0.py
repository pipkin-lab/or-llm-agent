from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

W = [1, 2, 3, 4]
K = [2, 3, 4]
N = 12

c = dict()
c[1, 2] = 18
c[1, 3] = 16
c[1, 4] = 12
c[2, 2] = 38
c[2, 3] = 36
c[2, 4] = 30
c[3, 2] = 14
c[3, 3] = 12
c[3, 4] = 11
c[4, 2] = 34
c[4, 3] = 31
c[4, 4] = 25

x = dict()
for w in W:
    for k in K:
        x[w, k] = solver.BoolVar('x_' + str(w) + '_' + str(k))

# Constraint 1: Exactly one assignment level per warehouse
for w in W:
    solver.Add(sum(x[w, k] for k in K) == 1)

# Constraint 2: Total patrol units equals 12
solver.Add(sum(k * x[w, k] for w in W for k in K) == N)

# Objective: Minimize total expected accidents
objective = sum(c[w, k] * x[w, k] for w in W for k in K)
solver.Minimize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")