from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Decision variables
    x1 = solver.NumVar(0, INF, 'x1')
    x2 = solver.NumVar(0, INF, 'x2')
    x3 = solver.NumVar(0, INF, 'x3')

    y1 = solver.BoolVar('y1')
    y2 = solver.BoolVar('y2')
    y3 = solver.BoolVar('y3')

    # Objective: Maximize total profit
    solver.Maximize(2000 * x1 + 3000 * x2 + 4000 * x3)

    # Steel constraint: 1.5*x1 + 3.0*x2 + 5.0*x3 <= 6000
    solver.Add(1.5 * x1 + 3.0 * x2 + 5.0 * x3 <= 6000)

    # Labor constraint: 300*x1 + 250*x2 + 400*x3 <= 600000
    solver.Add(300 * x1 + 250 * x2 + 400 * x3 <= 600000)

    # Linking constraints (upper bounds via binary)
    solver.Add(x1 <= 2000 * y1)
    solver.Add(x2 <= 2000 * y2)
    solver.Add(x3 <= 1200 * y3)

    # Minimum batch size constraints (lower bounds via binary)
    solver.Add(x1 >= 1000 * y1)
    solver.Add(x2 >= 1000 * y2)
    solver.Add(x3 >= 1000 * y3)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()