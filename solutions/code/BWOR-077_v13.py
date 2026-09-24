from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    W = [1, 2, 3, 4, 5]
    S = [1, 2, 3, 4, 5]

    E = dict()
    E[(1, 1)] = 2
    E[(1, 2)] = 3
    E[(1, 3)] = 4
    E[(1, 4)] = 1
    E[(1, 5)] = 7
    E[(2, 1)] = 3
    E[(2, 2)] = 4
    E[(2, 3)] = 2
    E[(2, 4)] = 5
    E[(2, 5)] = 6
    E[(3, 1)] = 2
    E[(3, 2)] = 5
    E[(3, 3)] = 3
    E[(3, 4)] = 4
    E[(3, 5)] = 1
    E[(4, 1)] = 5
    E[(4, 2)] = 2
    E[(4, 3)] = 3
    E[(4, 4)] = 2
    E[(4, 5)] = 5
    E[(5, 1)] = 3
    E[(5, 2)] = 7
    E[(5, 3)] = 6
    E[(5, 4)] = 2
    E[(5, 5)] = 4

    x = dict()
    for w in W:
        for s in S:
            x[w, s] = solver.BoolVar('x_' + str(w) + '_' + str(s))

    Z = solver.NumVar(0, INF, 'Z')

    for w in W:
        solver.Add(sum(x[w, s] for s in S) == 1)

    for s in S:
        solver.Add(sum(x[w, s] for w in W) == 1)

    for s in S:
        solver.Add(sum(E[w, s] * x[w, s] for w in W) >= Z)

    solver.Maximize(Z)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()