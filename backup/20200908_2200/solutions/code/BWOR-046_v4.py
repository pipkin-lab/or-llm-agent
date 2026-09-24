from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Parameters
    I = [1, 2, 3]
    J = [1, 2, 3, 4, 5]

    C = {
        (1, 1): 10, (1, 2): 15, (1, 3): 20, (1, 4): 20, (1, 5): 40,
        (2, 1): 20, (2, 2): 40, (2, 3): 15, (2, 4): 30, (2, 5): 30,
        (3, 1): 30, (3, 2): 35, (3, 3): 40, (3, 4): 55, (3, 5): 25
    }

    S = {1: 50, 2: 100, 3: 150}
    D = {1: 25, 2: 105, 3: 60, 4: 30, 5: 70}
    P = 270

    # Decision Variables
    x = {}
    for i in I:
        for j in J:
            x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

    # Objective Function
    obj_terms = []
    for i in I:
        for j in J:
            obj_terms.append(C[i, j] * x[i, j])
    solver.Minimize(sum(obj_terms))

    # Constraints
    # 1. Warehouse Capacity Constraints
    for i in I:
        solver.Add(sum(x[i, j] for j in J) <= S[i])

    # 2. Factory Production Constraint (Equality: Ship exactly 270 tons)
    total_shipped = sum(x[i, j] for i in I for j in J)
    solver.Add(total_shipped == P)

    # 3. Regional Demand Constraints
    for j in J:
        solver.Add(sum(x[i, j] for i in I) <= D[j])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()