from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("NO_FEASIBLE_SOLUTION")
        return

    INF = solver.infinity()

    # Decision variables
    x = dict()
    for j in range(1, 4):
        x[j] = solver.NumVar(0, INF, 'x_' + str(j))

    # Deviation variables
    d_neg = dict()
    d_pos = dict()
    for i in range(1, 6):
        d_neg[i] = solver.NumVar(0, INF, 'd_neg_' + str(i))
        d_pos[i] = solver.NumVar(0, INF, 'd_pos_' + str(i))

    # Parameters
    a = dict()
    a[1, 1] = 1; a[1, 2] = 1; a[1, 3] = 10
    a[2, 1] = 100; a[2, 2] = 10; a[2, 3] = 10
    a[3, 1] = 10; a[3, 2] = 100; a[3, 3] = 10

    R = dict()
    R[1] = 1
    R[2] = 30
    R[3] = 10

    c = dict()
    c[1] = 70
    c[2] = 50
    c[3] = 120

    p = dict()
    p[1] = 1.5
    p[2] = 8
    p[3] = 4

    # Constraints
    # Vitamin A goal
    solver.Add(1 * x[1] + 1 * x[2] + 10 * x[3] + d_neg[1] - d_pos[1] == 1)
    # Vitamin C goal
    solver.Add(100 * x[1] + 10 * x[2] + 10 * x[3] + d_neg[2] - d_pos[2] == 30)
    # Vitamin D goal
    solver.Add(10 * x[1] + 100 * x[2] + 10 * x[3] + d_neg[3] - d_pos[3] == 10)
    # Cholesterol goal
    solver.Add(70 * x[1] + 50 * x[2] + 120 * x[3] + d_neg[4] - d_pos[4] == 0)
    # Cost goal
    solver.Add(1.5 * x[1] + 8 * x[2] + 4 * x[3] + d_neg[5] - d_pos[5] == 0)

    # Phase 1: Minimize vitamin shortages
    obj1 = d_neg[1] + d_neg[2] + d_neg[3]
    solver.Minimize(obj1)
    status1 = solver.Solve()
    if status1 != pywraplp.Solver.OPTIMAL:
        print("NO_FEASIBLE_SOLUTION")
        return
    val1 = solver.Objective().Value()

    # Fix Phase 1 objective
    solver.Add(obj1 == val1)

    # Phase 2: Minimize cholesterol (d_pos[4])
    obj2 = d_pos[4]
    solver.Minimize(obj2)
    status2 = solver.Solve()
    if status2 != pywraplp.Solver.OPTIMAL:
        print("NO_FEASIBLE_SOLUTION")
        return
    val2 = solver.Objective().Value()

    # Fix Phase 2 objective
    solver.Add(obj2 == val2)

    # Phase 3: Minimize cost (d_pos[5])
    obj3 = d_pos[5]
    solver.Minimize(obj3)
    status3 = solver.Solve()
    if status3 != pywraplp.Solver.OPTIMAL:
        print("NO_FEASIBLE_SOLUTION")
        return
    val3 = solver.Objective().Value()

    # The final result to report is the minimized cost
    print("OPTIMAL_VALUE:", val3)

solve()