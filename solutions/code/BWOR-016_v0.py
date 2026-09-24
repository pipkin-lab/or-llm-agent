from ortools.linear_solver import pywraplp

def solve_factory_location():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index sets
    I = [1, 2, 3, 4]
    J = [1, 2, 3, 4]

    # Parameters
    c = dict()
    c[1, 1] = 2
    c[1, 2] = 9
    c[1, 3] = 3
    c[1, 4] = 4
    c[2, 1] = 8
    c[2, 2] = 3
    c[2, 3] = 5
    c[2, 4] = 7
    c[3, 1] = 7
    c[3, 2] = 6
    c[3, 3] = 1
    c[3, 4] = 2
    c[4, 1] = 4
    c[4, 2] = 5
    c[4, 3] = 2
    c[4, 4] = 5

    S = dict()
    S[1] = 400
    S[2] = 600
    S[3] = 200
    S[4] = 200

    D = dict()
    D[1] = 350
    D[2] = 400
    D[3] = 300
    D[4] = 150

    F = dict()
    F[1] = 0
    F[2] = 0
    F[3] = 1200
    F[4] = 1500

    # Decision variables
    x = dict()
    for i in I:
        for j in J:
            x[i, j] = solver.NumVar(0, INF, 'x_%d_%d' % (i, j))

    y = dict()
    y[3] = solver.BoolVar('y_3')
    y[4] = solver.BoolVar('y_4')

    # Objective: Minimize total cost
    obj_terms = []
    for i in I:
        for j in J:
            obj_terms.append(c[i, j] * x[i, j])
    obj_terms.append(F[3] * y[3])
    obj_terms.append(F[4] * y[4])
    solver.Minimize(sum(obj_terms))

    # Demand satisfaction constraints
    for j in J:
        solver.Add(sum(x[i, j] for i in I) == D[j])

    # Capacity constraints for existing factories (i=1, 2)
    for i in [1, 2]:
        solver.Add(sum(x[i, j] for j in J) <= S[i])

    # Capacity constraints for new factories (i=3, 4)
    for i in [3, 4]:
        solver.Add(sum(x[i, j] for j in J) <= S[i] * y[i])

    # Factory selection constraint: exactly one of A3 or A4 must be built
    solver.Add(y[3] + y[4] == 1)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_factory_location()