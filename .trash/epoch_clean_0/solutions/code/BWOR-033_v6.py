from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Index sets
    P = [1, 2, 3]
    T = [1, 2, 3, 4]

    # Parameters
    D = dict()
    D[1, 1] = 1500; D[1, 2] = 1000; D[1, 3] = 2000; D[1, 4] = 1200
    D[2, 1] = 1500; D[2, 2] = 1500; D[2, 3] = 1200; D[2, 4] = 1500
    D[3, 1] = 1000; D[3, 2] = 2000; D[3, 3] = 1500; D[3, 4] = 2500

    h = dict()
    h[1] = 2
    h[2] = 4
    h[3] = 3

    H = 15000

    c_inv = dict()
    c_inv[1] = 5
    c_inv[2] = 5
    c_inv[3] = 5

    c_late = dict()
    c_late[1] = 20
    c_late[2] = 20
    c_late[3] = 10

    I_end = 150

    # Decision variables
    x = dict()
    I = dict()
    B = dict()

    for p in P:
        for t in T:
            x[p, t] = solver.IntVar(0, inf, 'x_%d_%d' % (p, t))
            I[p, t] = solver.IntVar(0, inf, 'I_%d_%d' % (p, t))
            B[p, t] = solver.IntVar(0, inf, 'B_%d_%d' % (p, t))

    # Production restriction: Product 1 cannot be produced in Q2
    solver.Add(x[1, 2] == 0)

    # Inventory balance constraints
    for p in P:
        for t in T:
            if t == 1:
                I_prev = 0
                B_prev = 0
            else:
                I_prev = I[p, t - 1]
                B_prev = B[p, t - 1]

            solver.Add(I[p, t] - B[p, t] == I_prev - B_prev + x[p, t] - D[p, t])

    # Ending inventory and backlog conditions
    for p in P:
        solver.Add(I[p, 4] == I_end)
        solver.Add(B[p, 4] == 0)

    # Production capacity constraints
    Pt = dict()
    Pt[1] = [1, 2, 3]
    Pt[2] = [2, 3]
    Pt[3] = [1, 2, 3]
    Pt[4] = [1, 2, 3]

    for t in T:
        cap_expr = 0
        for p in Pt[t]:
            cap_expr += h[p] * x[p, t]
        solver.Add(cap_expr <= H)

    # Objective function
    obj_terms = []
    for p in P:
        for t in T:
            obj_terms.append(c_inv[p] * I[p, t])
            obj_terms.append(c_late[p] * B[p, t])

    solver.Minimize(sum(obj_terms))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()