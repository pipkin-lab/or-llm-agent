from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("NO_FEASIBLE_SOLUTION")
        return

    # Index sets
    I = range(1, 7)
    D = range(1, 6)

    # Parameters
    w = {1: 10.0, 2: 10.0, 3: 9.9, 4: 9.8, 5: 10.8, 6: 11.3}

    M = {
        (1, 1): 6, (2, 1): 0, (3, 1): 4, (4, 1): 5, (5, 1): 3, (6, 1): 0,
        (1, 2): 0, (2, 2): 9, (3, 2): 8, (4, 2): 5, (5, 2): 0, (6, 2): 9,
        (1, 3): 9, (2, 3): 0, (3, 3): 3, (4, 3): 6, (5, 3): 4, (6, 3): 0,
        (1, 4): 0, (2, 4): 6, (3, 4): 0, (4, 4): 0, (5, 4): 8, (6, 4): 6,
        (1, 5): 7, (2, 5): 0, (3, 5): 5, (4, 5): 4, (5, 5): 0, (6, 5): 3,
    }

    H = 14

    L = {1: 8, 2: 8, 3: 8, 4: 8, 5: 7, 6: 7}

    # Decision variables
    x = <curly_brackets></curly_brackets>
    for i in I:
        for d in D:
            x[i, d] = solver.NumVar(0, M[i, d], 'x_' + str(i) + '_' + str(d))

    # Objective: Minimize total weekly wage
    objective = 0
    for i in I:
        for d in D:
            objective += w[i] * x[i, d]

    solver.Minimize(objective)

    # Constraints

    # 1. Daily coverage: sum over i of x[i,d] == 14 for each d
    for d in D:
        solver.Add(sum(x[i, d] for i in I) == H)

    # 2. Maximum availability is already handled by variable upper bounds

    # 3. Minimum weekly work hours for each student
    for i in I:
        solver.Add(sum(x[i, d] for d in D) >= L[i])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve()