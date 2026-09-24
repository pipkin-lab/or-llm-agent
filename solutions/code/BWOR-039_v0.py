from ortools.linear_solver import pywraplp

def solve_production_plan():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    # Decision variables: x1 (bundles), x2 (dozens), x3 (boxes)
    x1 = solver.NumVar(0, INF, 'x1')
    x2 = solver.NumVar(0, INF, 'x2')
    x3 = solver.NumVar(0, INF, 'x3')

    # Objective: Maximize total profit
    solver.Maximize(2 * x1 + 3 * x2 + 1 * x3)

    # Labor constraint: x1 + x2 + x3 <= 3000
    solver.Add(x1 + x2 + x3 <= 3000)

    # Paper constraint: 10*x1 + 40*x2 + 80*x3 <= 90000
    solver.Add(10 * x1 + 40 * x2 + 80 * x3 <= 90000)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_plan()