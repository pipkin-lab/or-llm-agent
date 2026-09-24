from ortools.linear_solver import pywraplp

def solve():
    # Indices
    origins = [0, 1, 2]  # I, II, III
    destinations = [0, 1, 2, 3, 4]  # A, B, C, D, E

    # Parameters
    supply = [50, 100, 150]
    demand = [25, 115, 60, 30, 70]

    cost = [
        [10, 15, 20, 20, 40],
        [20, 10, 15, 30, 30],
        [30, 35, 40, 55, 25]
    ]

    # Create the LP solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("Could not create solver")
        return

    infinity = solver.infinity()

    # Decision variables x[i][j]
    x = dict()
    for i in origins:
        for j in destinations:
            x[i, j] = solver.NumVar(0, infinity, 'x_' + str(i) + '_' + str(j))

    # Objective function
    obj_terms = []
    for i in origins:
        for j in destinations:
            obj_terms.append(cost[i][j] * x[i, j])
    solver.Minimize(solver.Sum(obj_terms))

    # Supply constraints
    for i in origins:
        solver.Add(solver.Sum(x[i, j] for j in destinations) == supply[i])

    # Demand constraints
    for j in destinations:
        solver.Add(solver.Sum(x[i, j] for i in origins) == demand[j])

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()