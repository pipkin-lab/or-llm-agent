from ortools.linear_solver import pywraplp

def solve_maintenance():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    D = dict()
    D[1] = 100
    D[2] = 70
    D[3] = 80
    D[4] = 120
    D[5] = 150
    D[6] = 140

    x = dict()
    f = dict()
    s = dict()

    for t in range(1, 7):
        x[t] = solver.IntVar(0, INF, 'x_' + str(t))

    for t in range(1, 6):
        f[t] = solver.IntVar(0, INF, 'f_' + str(t))

    for t in range(1, 5):
        s[t] = solver.IntVar(0, INF, 's_' + str(t))

    # Objective: Minimize 10*x_t + 2*f_t + 10*s_t
    obj_terms = []
    for t in range(1, 7):
        obj_terms.append(10 * x[t])
    for t in range(1, 6):
        obj_terms.append(2 * f[t])
    for t in range(1, 5):
        obj_terms.append(10 * s[t])

    solver.Minimize(sum(obj_terms))

    # Demand satisfaction constraints
    # Period 1: x1 = D1
    solver.Add(x[1] == D[1])
    # Period 2: x2 + f1 = D2
    solver.Add(x[2] + f[1] == D[2])
    # Period 3: x3 + f2 + s1 = D3
    solver.Add(x[3] + f[2] + s[1] == D[3])
    # Period 4: x4 + f3 + s2 = D4
    solver.Add(x[4] + f[3] + s[2] == D[4])
    # Period 5: x5 + f4 + s3 = D5
    solver.Add(x[5] + f[4] + s[3] == D[5])
    # Period 6: x6 + f5 + s4 = D6
    solver.Add(x[6] + f[5] + s[4] == D[6])

    # Availability of used engines (repair source constraints)
    # Period 1: f1 + s1 <= D1
    solver.Add(f[1] + s[1] <= D[1])
    # Period 2: f2 + s2 <= D2
    solver.Add(f[2] + s[2] <= D[2])
    # Period 3: f3 + s3 <= D3
    solver.Add(f[3] + s[3] <= D[3])
    # Period 4: f4 + s4 <= D4
    solver.Add(f[4] + s[4] <= D[4])
    # Period 5: f5 <= D5 (s5 is not defined)
    solver.Add(f[5] <= D[5])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_maintenance()