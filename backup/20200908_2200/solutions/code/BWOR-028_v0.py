from ortools.linear_solver import pywraplp

def solve_nurse_scheduling():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Could not create solver")
        return

    # Parameters
    R = [10, 15, 25, 20, 18, 12]  # Requirements for periods 1 to 6
    n_shifts = 6
    n_periods = 6

    # Decision variables: number of nurses starting at each shift
    x = {}
    for s in range(n_shifts):
        x[s] = solver.IntVar(0, solver.infinity(), f'x_{s}')

    # Objective: minimize total nurses
    solver.Minimize(sum(x[s] for s in range(n_shifts)))

    # Constraints: coverage for each period
    # Period 1 (2:00-6:00): Shift 1 and Shift 6
    solver.Add(x[0] + x[5] >= R[0])
    # Period 2 (6:00-10:00): Shift 1 and Shift 2
    solver.Add(x[0] + x[1] >= R[1])
    # Period 3 (10:00-14:00): Shift 2 and Shift 3
    solver.Add(x[1] + x[2] >= R[2])
    # Period 4 (14:00-18:00): Shift 3 and Shift 4
    solver.Add(x[2] + x[3] >= R[3])
    # Period 5 (18:00-22:00): Shift 4 and Shift 5
    solver.Add(x[3] + x[4] >= R[4])
    # Period 6 (22:00-2:00): Shift 5 and Shift 6
    solver.Add(x[4] + x[5] >= R[5])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_nurse_scheduling()