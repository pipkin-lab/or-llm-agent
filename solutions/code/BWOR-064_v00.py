from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x[i, j]
plans = {
    1: [1, 2, 3],
    2: [1, 2, 3, 4],
    3: [1, 2]
}

costs = {
    (1, 1): 0, (1, 2): 1, (1, 3): 2,
    (2, 1): 0, (2, 2): 2, (2, 3): 3, (2, 4): 4,
    (3, 1): 0, (3, 2): 1
}

returns = {
    (1, 1): 0, (1, 2): 5, (1, 3): 6,
    (2, 1): 0, (2, 2): 8, (2, 3): 9, (2, 4): 12,
    (3, 1): 0, (3, 2): 3
}

x = dict()
for i in [1, 2, 3]:
    for j in plans[i]:
        x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))

# Objective: maximize total return
obj = 0
for i in [1, 2, 3]:
    for j in plans[i]:
        obj += returns[i, j] * x[i, j]

solver.Maximize(obj)

# Constraint 1: Budget limit
budget_expr = 0
for i in [1, 2, 3]:
    for j in plans[i]:
        budget_expr += costs[i, j] * x[i, j]
solver.Add(budget_expr <= 5)

# Constraint 2: Exactly one plan per factory
for i in [1, 2, 3]:
    solver.Add(sum(x[i, j] for j in plans[i]) == 1)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")