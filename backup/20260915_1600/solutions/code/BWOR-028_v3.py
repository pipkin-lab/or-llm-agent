from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    S = [1, 2, 3, 4, 5, 6]
    T = [1, 2, 3, 4, 5, 6]

    D = dict()
    D[1] = 10
    D[2] = 15
    D[3] = 25
    D[4] = 20
    D[5] = 18
    D[6] = 12

    x = dict()
    for s in S:
        x[s] = solver.IntVar(0, INF, 'x_' + str(s))

    # Coverage constraints based on the given matrix A
    # Period 1: x1 + x6 >= 10
    solver.Add(x[1] + x[6] >= D[1])
    # Period 2: x1 + x2 >= 15
    solver.Add(x[1] + x[2] >= D[2])
    # Period 3: x2 + x3 >= 25
    solver.Add(x[2] + x[3] >= D[3])
    # Period 4: x3 + x4 >= 20
    solver.Add(x[3] + x[4] >= D[4])
    # Period 5: x4 + x5 >= 18
    solver.Add(x[4] + x[5] >= D[5])
    # Period 6: x5 + x6 >= 12
    solver.Add(x[5] + x[6] >= D[6])

    obj = sum(x[s] for s in S)
    solver.Minimize(obj)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()