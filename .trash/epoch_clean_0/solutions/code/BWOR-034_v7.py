from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Index sets
    T = [1, 2, 3, 4]
    D = [1, 2, 3, 4]

    # Parameters
    R = dict()
    R[1] = 1500
    R[2] = 1000
    R[3] = 2000
    R[4] = 1200

    c = dict()
    c[1] = 28
    c[2] = 45
    c[3] = 60
    c[4] = 73

    # Decision variables: x[t, d] for valid (t, d) pairs where t + d - 1 <= 4
    x = dict()
    for t in T:
        for d in D:
            if t + d - 1 <= 4:
                x[t, d] = solver.NumVar(0, solver.infinity(), 'x_' + str(t) + '_' + str(d))

    # Objective function: minimize total rental cost
    obj = 0
    for t in T:
        for d in D:
            if t + d - 1 <= 4:
                obj += c[d] * x[t, d]

    solver.Minimize(obj)

    # Demand satisfaction constraints
    for t in T:
        constraint = 0
        for tp in T:
            if tp <= t:
                for d in D:
                    if tp + d - 1 <= 4 and tp + d - 1 >= t:
                        constraint += x[tp, d]
        solver.Add(constraint >= R[t])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()