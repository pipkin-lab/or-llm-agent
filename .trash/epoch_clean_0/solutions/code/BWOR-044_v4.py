from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()

    I = [1, 2, 3]
    J = ['A', 'B', 'C']

    # Decision variables
    x = dict()
    for i in I:
        for j in J:
            x[i, j] = solver.IntVar(0, infinity, 'x_{}_{}'.format(i, j))

    y = dict()
    for i in I:
        y[i] = solver.IntVar(0, infinity, 'y_{}'.format(i))

    # Objective function
    c = {(1, 'A'): 1, (1, 'B'): 2, (1, 'C'): 2,
         (2, 'A'): 1, (2, 'B'): 4, (2, 'C'): 5,
         (3, 'A'): 2, (3, 'B'): 3, (3, 'C'): 3}
    s = {1: 5, 2: 4, 3: 3}

    objective_terms = [c[i, j] * x[i, j] for i in I for j in J]
    objective_terms += [s[i] * y[i] for i in I]
    solver.Minimize(sum(objective_terms))

    # Supply balance constraints
    S = {1: 20, 2: 40, 3: 30}
    for i in I:
        solver.Add(sum(x[i, j] for j in J) + y[i] <= S[i])

    # Demand satisfaction constraints
    D = {'A': 30, 'B': 20, 'C': 20}
    for j in J:
        solver.Add(sum(x[i, j] for i in I) == D[j])

    # Minimum shipping constraints
    M = {1: 0, 2: 38, 3: 27}
    for i in I:
        solver.Add(sum(x[i, j] for j in J) >= M[i])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()