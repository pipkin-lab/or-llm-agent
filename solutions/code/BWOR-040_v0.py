from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Decision variables
    x1 = solver.NumVar(0, INF, 'x1')  # bundles of manuscript paper
    x2 = solver.NumVar(0, INF, 'x2')  # dozens of diaries
    x3 = solver.NumVar(0, INF, 'x3')  # boxes of exercise books
    T = solver.IntVar(0, INF, 'T')    # number of temporary workers

    # Objective: Maximize net profit
    # Z = 2*x1 + 3*x2 + 1*x3 - 40*T
    objective = 2 * x1 + 3 * x2 + 1 * x3 - 40 * T
    solver.Maximize(objective)

    # Constraint 1: Labor capacity
    # x1 + x2 + x3 <= 3000 + 30*T
    solver.Add(x1 + x2 + x3 <= 3000 + 30 * T)

    # Constraint 2: Raw material
    # 10*x1 + 40*x2 + 80*x3 <= 90000
    solver.Add(10 * x1 + 40 * x2 + 80 * x3 <= 90000)

    # Solve
    status = solver.Solve()
    if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()