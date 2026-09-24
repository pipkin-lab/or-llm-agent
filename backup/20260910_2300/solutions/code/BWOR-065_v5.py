from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("No feasible solution")
        return

    T = [1, 2, 3, 4, 5, 6]

    d = dict()
    d[1] = 1
    d[2] = 2
    d[3] = 5
    d[4] = 3
    d[5] = 2
    d[6] = 1

    M = 4
    K = 3
    c_v = 10000
    c_f = 4000
    c_s = 1000
    I_0 = 0

    x = dict()
    I = dict()
    y = dict()

    for t in T:
        x[t] = solver.NumVar(0, M, 'x_' + str(t))
        I[t] = solver.NumVar(0, K, 'I_' + str(t))
        y[t] = solver.BoolVar('y_' + str(t))

    for t in T:
        if t == 1:
            prev_I = I_0
        else:
            prev_I = I[t - 1]
        solver.Add(I[t] == prev_I + x[t] - d[t])

    for t in T:
        solver.Add(x[t] <= M * y[t])

    solver.Add(I[6] == 0)

    obj = 0
    for t in T:
        obj += c_v * x[t] + c_f * y[t] + c_s * I[t]

    solver.Minimize(obj)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()