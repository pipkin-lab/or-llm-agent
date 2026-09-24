from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index sets
    J = [1, 2, 3]
    R = ['A', 'B', 'C']

    # Parameters
    b = dict()
    b['A'] = 500
    b['B'] = 300
    b['C'] = 100

    a = dict()
    a[('A', 1)] = 2
    a[('A', 2)] = 4
    a[('A', 3)] = 8
    a[('B', 1)] = 2
    a[('B', 2)] = 3
    a[('B', 3)] = 4
    a[('C', 1)] = 1
    a[('C', 2)] = 2
    a[('C', 3)] = 3

    c = dict()
    c[1] = 4
    c[2] = 5
    c[3] = 6

    f = dict()
    f[1] = 100
    f[2] = 150
    f[3] = 200

    U = dict()
    U[1] = 100
    U[2] = 50
    U[3] = 100.0 / 3.0

    # Variables
    x = dict()
    for j in J:
        x[j] = solver.NumVar(0, INF, 'x_' + str(j))

    y = dict()
    for j in J:
        y[j] = solver.BoolVar('y_' + str(j))

    # Objective: Maximize total profit
    obj = 0
    for j in J:
        obj += c[j] * x[j] - f[j] * y[j]
    solver.Maximize(obj)

    # Resource constraints
    for r in R:
        expr = 0
        for j in J:
            expr += a[(r, j)] * x[j]
        solver.Add(expr <= b[r])

    # Big-M linking constraints
    for j in J:
        solver.Add(x[j] <= U[j] * y[j])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

main()