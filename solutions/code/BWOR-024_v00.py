from ortools.linear_solver import pywraplp

def solve_flow_shop():
    n = 6
    A = [0, 30, 60, 60, 20, 80, 90]  # 1-indexed
    B = [0, 70, 70, 50, 60, 30, 40]  # 1-indexed

    INF = 100000

    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise RuntimeError("SCIP solver not available")

    # x[j][k] = 1 if job j is in position k
    x = dict()
    for j in range(1, n + 1):
        for k in range(1, n + 1):
            x[j, k] = solver.BoolVar('x_{}_{}'.format(j, k))

    # CA[k] = cumulative completion time on Machine A after position k
    CA = dict()
    for k in range(1, n + 1):
        CA[k] = solver.NumVar(0, INF, 'CA_{}'.format(k))

    # CB[k] = cumulative completion time on Machine B after position k
    CB = dict()
    for k in range(1, n + 1):
        CB[k] = solver.NumVar(0, INF, 'CB_{}'.format(k))

    # Z = makespan = CB[n]
    Z = solver.NumVar(0, INF, 'Z')

    # Assignment: each job in exactly one position
    for j in range(1, n + 1):
        solver.Add(sum(x[j, k] for k in range(1, n + 1)) == 1)

    # Assignment: each position has exactly one job
    for k in range(1, n + 1):
        solver.Add(sum(x[j, k] for j in range(1, n + 1)) == 1)

    # Machine A completion times (linear, no max)
    for k in range(1, n + 1):
        if k == 1:
            solver.Add(CA[1] == sum(A[j] * x[j, 1] for j in range(1, n + 1)))
        else:
            solver.Add(CA[k] == CA[k - 1] + sum(A[j] * x[j, k] for j in range(1, n + 1)))

    # Machine B completion times with max(CA[k], CB[k-1]) + B_j*x_jk
    # We need to model: CB[k] = max(CA[k], CB[k-1]) + sum_j B_j * x[j,k]
    # Introduce auxiliary variable M_k = max(CA[k], CB[k-1])
    # Then CB[k] = M_k + sum_j B_j * x[j,k]
    # M_k >= CA[k], M_k >= CB[k-1] (for k>1), M_k >= 0
    # And to force M_k = max, we use: M_k <= CA[k] + M_BIG * (1 - y_k) and M_k <= CB[k-1] + M_BIG * y_k
    # where y_k is binary. But actually, since M_k is minimized implicitly (it's part of CB which we minimize),
    # we can just use M_k >= CA[k] and M_k >= CB[k-1] and let the objective push it down.
    # However, CB[k] depends on M_k, and we minimize Z = CB[n], so M_k will be at its minimum feasible value
    # which is max(CA[k], CB[k-1]). This works because increasing M_k only increases CB and thus Z.
    # So we just need:
    #   M_k >= CA[k]
    #   M_k >= CB[k-1]  (for k > 1)
    #   CB[k] = M_k + sum_j B_j * x[j,k]

    M = dict()
    for k in range(1, n + 1):
        M[k] = solver.NumVar(0, INF, 'M_{}'.format(k))

    for k in range(1, n + 1):
        solver.Add(M[k] >= CA[k])
        if k > 1:
            solver.Add(M[k] >= CB[k - 1])
        solver.Add(CB[k] == M[k] + sum(B[j] * x[j, k] for j in range(1, n + 1)))

    # Makespan
    solver.Add(Z == CB[n])

    # Objective: minimize Z
    solver.Minimize(Z)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve_flow_shop()