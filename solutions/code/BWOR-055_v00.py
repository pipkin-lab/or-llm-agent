from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Decision variables
    x1 = solver.NumVar(0, inf, 'x1')
    x2 = solver.NumVar(0, inf, 'x2')
    x3 = solver.NumVar(0, inf, 'x3')

    y1 = solver.BoolVar('y1')
    y2 = solver.BoolVar('y2')
    y3 = solver.BoolVar('y3')

    # Objective: Maximize 60*x1 + 40*x2 + 100*x3 - 2000*y1 - 1500*y2 - 1000*y3
    objective = 60 * x1 + 40 * x2 + 100 * x3 - 2000 * y1 - 1500 * y2 - 1000 * y3
    solver.Maximize(objective)

    # Resource constraints
    solver.Add(3 * x1 + 2 * x2 + 6 * x3 <= 150)  # Labor
    solver.Add(4 * x1 + 3 * x2 + 6 * x3 <= 160)  # Material

    # Linking constraints (Big-M)
    solver.Add(x1 <= 40 * y1)
    solver.Add(x2 <= 53 * y2)
    solver.Add(x3 <= 25 * y3)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()