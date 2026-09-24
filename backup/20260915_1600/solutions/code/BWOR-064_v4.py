from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
I = [1, 2, 3]
J = {
    1: [2, 3],
    2: [2, 3, 4],
    3: [2]
}

# Parameters: investment cost c[i][j] and return r[i][j]
c = dict()
r = dict()
c[(1, 2)] = 1
r[(1, 2)] = 5
c[(1, 3)] = 2
r[(1, 3)] = 6
c[(2, 2)] = 2
r[(2, 2)] = 8
c[(2, 3)] = 3
r[(2, 3)] = 9
c[(2, 4)] = 4
r[(2, 4)] = 12
c[(3, 2)] = 1
r[(3, 2)] = 3

B = 5

# Decision variables: x[i, j] binary for each factory i and plan j in J[i]
x = dict()
for i in I:
    for j in J[i]:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: maximize total return
obj = sum(r[i, j] * x[i, j] for i in I for j in J[i])
solver.Maximize(obj)

# Constraint 1: Budget
solver.Add(sum(c[i, j] * x[i, j] for i in I for j in J[i]) <= B)

# Constraint 2: At most one plan per factory
for i in I:
    solver.Add(sum(x[i, j] for j in J[i]) <= 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")