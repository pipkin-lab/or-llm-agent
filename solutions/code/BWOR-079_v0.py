from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Decision variables: x[d] for d in 1..7 (integer, non-negative)
    x = dict()
    for d in range(1, 8):
        x[d] = solver.IntVar(0, INF, 'x_' + str(d))

    # Objective: minimize total nurses
    obj_terms = []
    for d in range(1, 8):
        obj_terms.append(x[d])
    solver.Minimize(sum(obj_terms))

    # Demand parameters
    R = dict()
    R[1] = 18
    R[2] = 20
    R[3] = 19
    R[4] = 17
    R[5] = 12

    # Coverage matrix A[p][s], 1-indexed
    # Rows: periods 1-5, Cols: shifts 1-5
    A = dict()
    A[1, 1] = 1; A[1, 2] = 1; A[1, 3] = 0; A[1, 4] = 0; A[1, 5] = 0
    A[2, 1] = 0; A[2, 2] = 1; A[2, 3] = 1; A[2, 4] = 0; A[2, 5] = 0
    A[3, 1] = 0; A[3, 2] = 0; A[3, 3] = 1; A[3, 4] = 1; A[3, 5] = 0
    A[4, 1] = 0; A[4, 2] = 0; A[4, 3] = 0; A[4, 4] = 1; A[4, 5] = 1
    A[5, 1] = 1; A[5, 2] = 0; A[5, 3] = 0; A[5, 4] = 0; A[5, 5] = 1

    # Helper to compute the start-day index k for a given day d and shift s
    # k ≡ d - (s - 1) (mod 7), mapped to 1..7
    def mod7(val):
        # Map integer to 1..7 range for mod 7
        return ((val - 1) % 7) + 1

    # For each day d (1..7) and each period p (1..5), build the constraint
    # Nurses on duty for period p on day d = sum_s A[p,s] * Y[d,s] >= R[p]
    # where Y[d,s] = x[k] with k = mod7(d - (s-1))
    for d in range(1, 8):
        for p in range(1, 6):
            expr = 0
            for s in range(1, 6):
                if A[p, s] == 1:
                    k = mod7(d - (s - 1))
                    expr += x[k]
            solver.Add(expr >= R[p])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()