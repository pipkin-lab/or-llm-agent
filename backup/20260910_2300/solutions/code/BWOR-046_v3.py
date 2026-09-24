from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("No solver found")
        return

    # Index sets
    I = [1, 2, 3]
    J = [1, 2, 3, 4, 5]

    # Parameters
    S_max = 270
    C = dict()
    C[1] = 50
    C[2] = 100
    C[3] = 150

    D = dict()
    D[1] = 25
    D[2] = 105
    D[3] = 60
    D[4] = 30
    D[5] = 70

    c = dict()
    # From Warehouse A1
    c[1, 1] = 10
    c[1, 2] = 15
    c[1, 3] = 20
    c[1, 4] = 20
    c[1, 5] = 40
    # From Warehouse A2
    c[2, 1] = 20
    c[2, 2] = 40
    c[2, 3] = 15
    c[2, 4] = 30
    c[2, 5] = 30
    # From Warehouse A3
    c[3, 1] = 30
    c[3, 2] = 35
    c[3, 3] = 40
    c[3, 4] = 55
    c[3, 5] = 25

    # Decision variables
    x = dict()
    for i in I:
        for j in J:
            x[i, j] = solver.NumVar(0, solver.infinity(), 'x_{}{}'.format(i, j))

    # Objective: Minimize total cost
    objective_terms = []
    for i in I:
        for j in J:
            objective_terms.append(c[i, j] * x[i, j])
    solver.Minimize(sum(objective_terms))

    # Constraints
    # 1. Warehouse Capacity
    for i in I:
        cap_expr = sum(x[i, j] for j in J)
        solver.Add(cap_expr <= C[i])

    # 2. Factory Production Capacity
    total_shipped = sum(x[i, j] for i in I for j in J)
    solver.Add(total_shipped <= S_max)

    # 3. Regional Demand (Equality as per standard formulation, though potentially infeasible given data)
    for j in J:
        demand_expr = sum(x[i, j] for i in I)
        solver.Add(demand_expr == D[j])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve()