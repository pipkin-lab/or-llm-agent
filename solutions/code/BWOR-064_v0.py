from ortools.linear_solver import pywraplp

# Index sets
I = [1, 2, 3]
J = {
    1: [1, 2, 3],
    2: [1, 2, 3, 4],
    3: [1, 2]
}

# Parameters
B = 5
c = dict()
r = dict()
c[(1, 1)] = 0; r[(1, 1)] = 0
c[(1, 2)] = 1; r[(1, 2)] = 5
c[(1, 3)] = 2; r[(1, 3)] = 6
c[(2, 1)] = 0; r[(2, 1)] = 0
c[(2, 2)] = 2; r[(2, 2)] = 8
c[(2, 3)] = 3; r[(2, 3)] = 9
c[(2, 4)] = 4; r[(2, 4)] = 12
c[(3, 1)] = 0; r[(3, 1)] = 0
c[(3, 2)] = 1; r[(3, 2)] = 3

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x = dict()
for i in I:
    for j in J[i]:
        x[(i, j)] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: maximize total return
obj = 0
for i in I:
    for j in J[i]:
        obj += r[(i, j)] * x[(i, j)]
solver.Maximize(obj)

# Constraint 1: exactly one plan per factory
for i in I:
    solver.Add(sum(x[(i, j)] for j in J[i]) == 1)

# Constraint 2: budget
total_cost = 0
for i in I:
    for j in J[i]:
        total_cost += c[(i, j)] * x[(i, j)]
solver.Add(total_cost <= B)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")