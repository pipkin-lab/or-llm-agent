from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Decision variables: x_i in {0, 1} for i in 1..7
    x = dict()
    for i in range(1, 8):
        x[i] = solver.BoolVar('x_' + str(i))

    # Objective: minimize sum of x_i
    obj = 0
    for i in range(1, 8):
        obj += x[i]
    solver.Minimize(obj)

    # Category coverage constraints
    # Math (k=1): x1 + x2 + x3 + x4 + x7 >= 2
    solver.Add(x[1] + x[2] + x[3] + x[4] + x[7] >= 2)

    # OR (k=2): x2 + x4 + x5 + x7 >= 2
    solver.Add(x[2] + x[4] + x[5] + x[7] >= 2)

    # CS (k=3): x3 + x5 + x6 >= 2
    solver.Add(x[3] + x[5] + x[6] >= 2)

    # Prerequisite constraints
    # x5 <= x6
    solver.Add(x[5] <= x[6])
    # x3 <= x6
    solver.Add(x[3] <= x[6])
    # x4 <= x1
    solver.Add(x[4] <= x[1])
    # x7 <= x4
    solver.Add(x[7] <= x[4])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()