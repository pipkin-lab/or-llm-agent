from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameter definitions
investment = dict()
ret = dict()

investment[(1, 1)] = 0
ret[(1, 1)] = 0
investment[(1, 2)] = 1
ret[(1, 2)] = 5
investment[(1, 3)] = 2
ret[(1, 3)] = 6

investment[(2, 1)] = 0
ret[(2, 1)] = 0
investment[(2, 2)] = 2
ret[(2, 2)] = 8
investment[(2, 3)] = 3
ret[(2, 3)] = 9
investment[(2, 4)] = 4
ret[(2, 4)] = 12

investment[(3, 1)] = 0
ret[(3, 1)] = 0
investment[(3, 2)] = 1
ret[(3, 2)] = 3

# Available plans per factory
plans = dict()
plans[1] = [1, 2, 3]
plans[2] = [1, 2, 3, 4]
plans[3] = [1, 2]

# Decision variables
x = dict()
for i in [1, 2, 3]:
    for j in plans[i]:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective function
obj = 0
for i in [1, 2, 3]:
    for j in plans[i]:
        obj += ret[(i, j)] * x[i, j]

solver.Maximize(obj)

# Constraints: One plan per factory
for i in [1, 2, 3]:
    solver.Add(sum(x[i, j] for j in plans[i]) == 1)

# Budget constraint
budget = 5
total_investment = 0
for i in [1, 2, 3]:
    for j in plans[i]:
        total_investment += investment[(i, j)] * x[i, j]

solver.Add(total_investment <= budget)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")