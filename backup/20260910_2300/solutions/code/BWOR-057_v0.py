from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print("NO_SOLVER_CREATED")
        return None

    I = [1, 2, 3, 4, 5, 6]
    C = {1: 1500, 2: 2500, 3: 4000, 4: 6000, 5: 9000, 6: 12000}
    D = {1: 500, 2: 550, 3: 700, 4: 900, 5: 400, 6: 300}
    v = {1: 5, 2: 8, 3: 10, 4: 12, 5: 16, 6: 18}
    F = 1200

    # Define substitution sets
    S = {}
    for i in I:
        S[i] = [j for j in I if C[j] >= C[i]]

    # Decision variables
    x = dict()
    for i in I:
        for j in I:
            if j in S[i]:
                x[i, j] = solver.IntVar(0, solver.infinity(), 'x_{}_{}'.format(i, j))
            else:
                x[i, j] = 0  # Not allowed

    y = dict()
    for j in I:
        y[j] = solver.BoolVar('y_{}'.format(j))

    # Objective function
    obj_terms = []
    for i in I:
        for j in I:
            if j in S[i]:
                obj_terms.append(v[j] * x[i, j])
    for j in I:
        obj_terms.append(F * y[j])
    solver.Minimize(sum(obj_terms))

    # Demand satisfaction constraints
    for i in I:
        constraint = sum(x[i, j] for j in S[i]) >= D[i]
        solver.Add(constraint)

    # Machine activation linking constraints (Big-M)
    M = sum(D.values())  # 3350
    for j in I:
        constraint = sum(x[i, j] for i in I) <= M * y[j]
        solver.Add(constraint)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()