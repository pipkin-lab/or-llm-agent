from ortools.linear_solver import pywraplp

def solve_renovation_problem():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        raise ValueError('SCIP solver not available')

    # Define index sets
    I = [1, 2, 3]
    J1 = [1, 2, 3]
    J2 = [1, 2, 3, 4]
    J3 = [1, 2]

    Ji = dict()
    Ji[1] = J1
    Ji[2] = J2
    Ji[3] = J3

    # Define parameters
    C = 5

    # Investment costs a[i][j]
    a = dict()
    a[1, 1] = 0
    a[1, 2] = 1
    a[1, 3] = 2
    a[2, 1] = 0
    a[2, 2] = 2
    a[2, 3] = 3
    a[2, 4] = 4
    a[3, 1] = 0
    a[3, 2] = 1

    # Returns r[i][j]
    r = dict()
    r[1, 1] = 0
    r[1, 2] = 5
    r[1, 3] = 6
    r[2, 1] = 0
    r[2, 2] = 8
    r[2, 3] = 9
    r[2, 4] = 12
    r[3, 1] = 0
    r[3, 2] = 3

    # Create binary decision variables
    x = dict()
    for i in I:
        for j in Ji[i]:
            x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

    # Single selection constraint: exactly one plan per factory
    for i in I:
        solver.Add(sum(x[i, j] for j in Ji[i]) == 1)

    # Budget constraint
    total_cost = 0
    for i in I:
        for j in Ji[i]:
            total_cost += a[i, j] * x[i, j]
    solver.Add(total_cost <= C)

    # Objective: maximize total return
    objective = 0
    for i in I:
        for j in Ji[i]:
            objective += r[i, j] * x[i, j]
    solver.Maximize(objective)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_renovation_problem()