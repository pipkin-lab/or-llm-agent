from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        raise RuntimeError('GLOP solver not available')

    # Index set K = {1, 2, 3, 4}
    K = [1, 2, 3, 4]

    # Frequency requirements f_k
    f = dict()
    f[1] = 3
    f[2] = 2
    f[3] = 1
    f[4] = 1

    # Time interval matrix I_{k,l}
    I = dict()
    I[1, 1] = 36
    I[1, 2] = 32
    I[1, 3] = 33
    I[1, 4] = 19
    I[2, 1] = 10
    I[2, 2] = 8
    I[2, 3] = 7
    I[2, 4] = 20
    I[3, 1] = 12
    I[3, 2] = 17
    I[3, 3] = 16
    I[3, 4] = 29
    I[4, 1] = 23
    I[4, 2] = 15
    I[4, 3] = 16
    I[4, 4] = 28

    # Decision variables y_{k,l} >= 0
    y = dict()
    for k in K:
        for l in K:
            y[k, l] = solver.NumVar(0, solver.infinity(), 'y_' + str(k) + '_' + str(l))

    # Outflow conservation: sum_l y_{k,l} = f_k
    for k in K:
        solver.Add(sum(y[k, l] for l in K) == f[k])

    # Inflow conservation: sum_k y_{k,l} = f_l
    for l in K:
        solver.Add(sum(y[k, l] for k in K) == f[l])

    # Objective: Minimize Z = sum_{k,l} I_{k,l} * y_{k,l}
    objective_terms = []
    for k in K:
        for l in K:
            objective_terms.append(I[k, l] * y[k, l])
    solver.Minimize(sum(objective_terms))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()