from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Index sets
    workshops = ['A', 'B', 'C', 'D', 'E']
    locations = ['U', 'alpha', 'beta']

    # Pairs with non-zero transport volume
    P = [('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'E')]

    # Parameters
    # Savings (10,000 yuan/year)
    S = dict()
    for i in workshops:
        for t in locations:
            S[i, t] = 0
    S['A', 'alpha'] = 100
    S['A', 'beta'] = 100
    S['B', 'alpha'] = 150
    S['B', 'beta'] = 200
    S['C', 'alpha'] = 100
    S['C', 'beta'] = 150
    S['D', 'alpha'] = 200
    S['D', 'beta'] = 150
    S['E', 'alpha'] = 50
    S['E', 'beta'] = 150

    # Transport volumes (tons/year)
    C_ik = dict()
    C_ik['A', 'C'] = 1000
    C_ik['A', 'D'] = 1500
    C_ik['B', 'C'] = 1400
    C_ik['B', 'D'] = 1200
    C_ik['C', 'E'] = 2000
    C_ik['D', 'E'] = 700

    # Transport rates D' (10,000 yuan/ton)
    D = dict()
    D['U', 'U'] = 0.1
    D['alpha', 'alpha'] = 0.05
    D['beta', 'beta'] = 0.05
    D['U', 'alpha'] = 0.13
    D['alpha', 'U'] = 0.13
    D['U', 'beta'] = 0.09
    D['beta', 'U'] = 0.09
    D['alpha', 'beta'] = 0.14
    D['beta', 'alpha'] = 0.14

    # Decision variables
    x = dict()
    for i in workshops:
        for t in locations:
            x[i, t] = solver.BoolVar('x_' + i + '_' + t)

    y = dict()
    for (i, k) in P:
        for j in locations:
            for l in locations:
                y[i, k, j, l] = solver.BoolVar('y_' + i + k + '_' + j + l)

    # Objective: Minimize total transport cost - total savings
    obj_expr = 0
    for (i, k) in P:
        for j in locations:
            for l in locations:
                obj_expr += C_ik[i, k] * D[j, l] * y[i, k, j, l]

    for i in workshops:
        for t in ['alpha', 'beta']:
            obj_expr -= S[i, t] * x[i, t]

    solver.Minimize(obj_expr)

    # Constraints
    # 1. Assignment: each workshop assigned to exactly one location
    for i in workshops:
        solver.Add(sum(x[i, t] for t in locations) == 1)

    # 2. Capacity: no more than 3 workshops per location
    for t in locations:
        solver.Add(sum(x[i, t] for i in workshops) <= 3)

    # 3. Linking constraints for y variables
    for (i, k) in P:
        for j in locations:
            for l in locations:
                y_var = y[i, k, j, l]
                x_ij = x[i, j]
                x_kl = x[k, l]
                solver.Add(y_var <= x_ij)
                solver.Add(y_var <= x_kl)
                solver.Add(y_var >= x_ij + x_kl - 1)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()