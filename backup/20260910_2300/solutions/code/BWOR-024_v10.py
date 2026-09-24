from ortools.linear_solver import pywraplp

def solve_flow_shop():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("NO_FEASIBLE_SOLUTION")
        return

    n = 6
    jobs = [1, 2, 3, 4, 5, 6]
    positions = [1, 2, 3, 4, 5, 6]

    a = dict()
    a[1] = 30
    a[2] = 60
    a[3] = 60
    a[4] = 20
    a[5] = 80
    a[6] = 90

    b = dict()
    b[1] = 70
    b[2] = 70
    b[3] = 50
    b[4] = 60
    b[5] = 30
    b[6] = 40

    x = dict()
    for j in jobs:
        for p in positions:
            x[j, p] = solver.BoolVar('x_' + str(j) + '_' + str(p))

    C_A = dict()
    for p in positions:
        C_A[p] = solver.NumVar(0, solver.infinity(), 'C_A_' + str(p))

    C_B = dict()
    for p in positions:
        C_B[p] = solver.NumVar(0, solver.infinity(), 'C_B_' + str(p))

    # Assignment constraints: each job assigned to exactly one position
    for j in jobs:
        solver.Add(sum(x[j, p] for p in positions) == 1)

    # Position constraints: each position holds exactly one job
    for p in positions:
        solver.Add(sum(x[j, p] for j in jobs) == 1)

    # Machine A completion times
    # For position 1: C_A(1) = sum_j a_j * x_{j,1}
    solver.Add(C_A[1] == sum(a[j] * x[j, 1] for j in jobs))

    # For positions 2..n: C_A(p) >= C_A(p-1) + sum_j a_j * x_{j,p}
    for p in positions[1:]:
        solver.Add(C_A[p] >= C_A[p - 1] + sum(a[j] * x[j, p] for j in jobs))

    # Machine B completion times
    # C_B(p) >= C_A(p) + sum_j b_j * x_{j,p} for all p
    for p in positions:
        solver.Add(C_B[p] >= C_A[p] + sum(b[j] * x[j, p] for j in jobs))

    # C_B(p) >= C_B(p-1) + sum_j b_j * x_{j,p} for p = 2..n
    for p in positions[1:]:
        solver.Add(C_B[p] >= C_B[p - 1] + sum(b[j] * x[j, p] for j in jobs))

    # Objective: minimize C_B(n)
    solver.Minimize(C_B[n])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_flow_shop()