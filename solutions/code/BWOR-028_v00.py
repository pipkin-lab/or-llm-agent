from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    x = dict()
    for j in range(1, 7):
        x[j] = solver.IntVar(0, INF, 'x_' + str(j))

    solver.Minimize(x[1] + x[2] + x[3] + x[4] + x[5] + x[6])

    solver.Add(x[6] + x[1] >= 10)
    solver.Add(x[1] + x[2] >= 15)
    solver.Add(x[2] + x[3] >= 25)
    solver.Add(x[3] + x[4] >= 20)
    solver.Add(x[4] + x[5] >= 18)
    solver.Add(x[5] + x[6] >= 12)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()