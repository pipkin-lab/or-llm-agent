from ortools.linear_solver import pywraplp

# Time matrix T[i, j]: Person i, Task j
persons = ['X', 'Y', 'Z', 'R']
tasks = ['A', 'B', 'C', 'D', 'F']

T = dict()
T[('X', 'A')] = 25
T[('X', 'B')] = 29
T[('X', 'C')] = 31
T[('X', 'D')] = 42
T[('X', 'F')] = 37
T[('Y', 'A')] = 39
T[('Y', 'B')] = 38
T[('Y', 'C')] = 26
T[('Y', 'D')] = 20
T[('Y', 'F')] = 33
T[('Z', 'A')] = 34
T[('Z', 'B')] = 27
T[('Z', 'C')] = 28
T[('Z', 'D')] = 40
T[('Z', 'F')] = 32
T[('R', 'A')] = 24
T[('R', 'B')] = 42
T[('R', 'C')] = 36
T[('R', 'D')] = 23
T[('R', 'F')] = 45


def solve_scenario_a():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = dict()
    for i in persons:
        for j in tasks:
            x[(i, j)] = solver.BoolVar('x_' + i + '_' + j)

    # Objective: minimize total time
    obj = sum(T[(i, j)] * x[(i, j)] for i in persons for j in tasks)
    solver.Minimize(obj)

    # Task assignment: all 5 tasks assigned
    for j in tasks:
        solver.Add(sum(x[(i, j)] for i in persons) == 1)

    # Person workload: each person 1 or 2 tasks
    for i in persons:
        solver.Add(sum(x[(i, j)] for j in tasks) <= 2)
        solver.Add(sum(x[(i, j)] for j in tasks) >= 1)

    # Total assignments = 5 (redundant with task constraints but explicit)
    solver.Add(sum(x[(i, j)] for i in persons for j in tasks) == 5)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        return solver.Objective().Value()
    else:
        return None


def solve_scenario_b():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = dict()
    for i in persons:
        for j in tasks:
            x[(i, j)] = solver.BoolVar('x_' + i + '_' + j)

    # Objective: minimize total time
    obj = sum(T[(i, j)] * x[(i, j)] for i in persons for j in tasks)
    solver.Minimize(obj)

    # Task assignment: all 5 tasks assigned
    for j in tasks:
        solver.Add(sum(x[(i, j)] for i in persons) == 1)

    # Person workload constraints
    # Y takes exactly 1 task
    solver.Add(sum(x[('Y', j)] for j in tasks) == 1)
    # R takes exactly 1 task
    solver.Add(sum(x[('R', j)] for j in tasks) == 1)
    # X takes 1 or 2 tasks
    solver.Add(sum(x[('X', j)] for j in tasks) <= 2)
    solver.Add(sum(x[('X', j)] for j in tasks) >= 1)
    # Z takes 1 or 2 tasks
    solver.Add(sum(x[('Z', j)] for j in tasks) <= 2)
    solver.Add(sum(x[('Z', j)] for j in tasks) >= 1)
    # X + Z together take exactly 3 tasks (one gets 2, other gets 1)
    solver.Add(sum(x[('X', j)] for j in tasks) + sum(x[('Z', j)] for j in tasks) == 3)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        return solver.Objective().Value()
    else:
        return None


def solve_scenario_c():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = dict()
    for i in persons:
        for j in tasks:
            x[(i, j)] = solver.BoolVar('x_' + i + '_' + j)

    # Objective: minimize total time
    obj = sum(T[(i, j)] * x[(i, j)] for i in persons for j in tasks)
    solver.Minimize(obj)

    # Person workload: each person takes exactly 1 task
    for i in persons:
        solver.Add(sum(x[(i, j)] for j in tasks) == 1)

    # Task constraints: A and B must be assigned
    solver.Add(sum(x[(i, 'A')] for i in persons) == 1)
    solver.Add(sum(x[(i, 'B')] for i in persons) == 1)
    # Exactly 2 of {C, D, F} assigned
    solver.Add(sum(x[(i, 'C')] for i in persons) + sum(x[(i, 'D')] for i in persons) + sum(x[(i, 'F')] for i in persons) == 2)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        return solver.Objective().Value()
    else:
        return None


def main():
    result_a = solve_scenario_a()
    result_b = solve_scenario_b()
    result_c = solve_scenario_c()

    if result_a is None or result_b is None or result_c is None:
        print("NO_FEASIBLE_SOLUTION")
        return

    print("OPTIMAL_VALUE:", result_a)
    print("OPTIMAL_VALUE:", result_b)
    print("OPTIMAL_VALUE:", result_c)


if __name__ == '__main__':
    main()