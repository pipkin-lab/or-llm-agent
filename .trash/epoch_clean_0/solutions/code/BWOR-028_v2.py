from ortools.linear_solver import pywraplp

def solve_nurse_staffing():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print("NO_FEASIBLE_SOLUTION")
        return

    # Index sets
    K = list(range(1, 7))

    # Demand parameters
    D = {1: 10, 2: 15, 3: 25, 4: 20, 5: 18, 6: 12}

    # Decision variables: x_k for k in K
    x = dict()
    for k in K:
        x[k] = solver.IntVar(0, solver.infinity(), 'x_{}'.format(k))

    # Objective: minimize total nurses
    objective = sum(x[k] for k in K)
    solver.Minimize(objective)

    # Constraints: for each period j, sum of x_k where S_{k,j} = 1 >= D_j
    # Period 1: x_6 + x_1 >= 10
    # Period 2: x_1 + x_2 >= 15
    # Period 3: x_2 + x_3 >= 25
    # Period 4: x_3 + x_4 >= 20
    # Period 5: x_4 + x_5 >= 18
    # Period 6: x_5 + x_6 >= 12
    for j in K:
        # Nurses on duty in period j are those who started at j and j-1 (with wrap-around)
        k_prev = j - 1 if j > 1 else 6
        constraint = x[k_prev] + x[j] >= D[j]
        solver.Add(constraint)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_nurse_staffing()