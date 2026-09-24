from ortools.linear_solver import pywraplp

def solve_workshop_location():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    W = ['A', 'B', 'C', 'D', 'E']
    L = ['alpha', 'beta', 'U']

    # Savings (yuan/year)
    S = dict()
    S[('A', 'alpha')] = 1000000
    S[('A', 'beta')] = 1000000
    S[('A', 'U')] = 0

    S[('B', 'alpha')] = 1500000
    S[('B', 'beta')] = 2000000
    S[('B', 'U')] = 0

    S[('C', 'alpha')] = 1000000
    S[('C', 'beta')] = 1500000
    S[('C', 'U')] = 0

    S[('D', 'alpha')] = 2000000
    S[('D', 'beta')] = 1500000
    S[('D', 'U')] = 0

    S[('E', 'alpha')] = 500000
    S[('E', 'beta')] = 1500000
    S[('E', 'U')] = 0

    # Transport volumes (t/year) - symmetric, only store i < k
    C = dict()
    C[('A', 'C')] = 1000
    C[('A', 'D')] = 1500
    C[('B', 'C')] = 1400
    C[('B', 'D')] = 1200
    C[('C', 'E')] = 2000
    C[('D', 'E')] = 700

    # Transport rates (yuan/t) - symmetric
    D = dict()
    D[('alpha', 'alpha')] = 500
    D[('alpha', 'beta')] = 1400
    D[('alpha', 'U')] = 1300
    D[('beta', 'alpha')] = 1400
    D[('beta', 'beta')] = 500
    D[('beta', 'U')] = 900
    D[('U', 'alpha')] = 1300
    D[('U', 'beta')] = 900
    D[('U', 'U')] = 1000

    # Decision variables x[i, l] - binary
    x = dict()
    for i in W:
        for l in L:
            x[i, l] = solver.BoolVar('x_{}_{}'.format(i, l))

    # Auxiliary variables w[i, k, j, l] - binary, for i < k
    pairs = [('A', 'C'), ('A', 'D'), ('A', 'B'), ('A', 'E'), ('B', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'D'), ('C', 'E'), ('D', 'E')]
    # Let's use a consistent ordering. W = [A, B, C, D, E]. i < k means index in W.
    W_index = {w: idx for idx, w in enumerate(W)}
    pairs = []
    for i in W:
        for k in W:
            if W_index[i] < W_index[k]:
                pairs.append((i, k))

    w = dict()
    for (i, k) in pairs:
        for j in L:
            for l in L:
                w[i, k, j, l] = solver.BoolVar('w_{}_{}_{}_{}'.format(i, k, j, l))

    # Objective Function
    obj_expr = 0
    # Transportation cost part
    for (i, k) in pairs:
        vol = C[(i, k)]
        for j in L:
            for l in L:
                rate = D[(j, l)]
                obj_expr += vol * rate * w[i, k, j, l]

    # Savings part (subtracted)
    for i in W:
        for l in L:
            obj_expr -= S[(i, l)] * x[i, l]

    solver.Minimize(obj_expr)

    # Constraints
    # 1. Assignment: each workshop in exactly one location
    for i in W:
        solver.Add(sum(x[i, l] for l in L) == 1)

    # 2. Capacity: max 3 workshops per location
    for l in L:
        solver.Add(sum(x[i, l] for i in W) <= 3)

    # 3. Linking constraints for w
    for (i, k) in pairs:
        for j in L:
            for l in L:
                # w[i,k,j,l] <= x[i,j]
                solver.Add(w[i, k, j, l] <= x[i, j])
                # w[i,k,j,l] <= x[k,l]
                solver.Add(w[i, k, j, l] <= x[k, l])
                # w[i,k,j,l] >= x[i,j] + x[k,l] - 1
                solver.Add(w[i, k, j, l] >= x[i, j] + x[k, l] - 1)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_workshop_location()