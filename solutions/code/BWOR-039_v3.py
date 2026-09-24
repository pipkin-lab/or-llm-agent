from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Decision variables: x_1, x_2, x_3 (integer, non-negative)
    x = dict()
    for i in [1, 2, 3]:
        x[i] = solver.IntVar(0, INF, 'x_' + str(i))

    # Objective: Maximize Z = 2*x1 + 3*x2 + 1*x3
    objective = 2 * x[1] + 3 * x[2] + 1 * x[3]
    solver.Maximize(objective)

    # Constraint 1: Labor: x1 + x2 + x3 <= 3000
    solver.Add(x[1] + x[2] + x[3] <= 3000)

    # Constraint 2: Material: x1 + 4*x2 + 8*x3 <= 9000
    solver.Add(x[1] + 4 * x[2] + 8 * x[3] <= 9000)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()