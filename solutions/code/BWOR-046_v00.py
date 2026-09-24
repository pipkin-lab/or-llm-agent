from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("No solver available")
        return

    INF = solver.infinity()

    # Index sets
    warehouses = [1, 2, 3]
    regions = [1, 2, 3, 4, 5]

    # Parameters
    # Warehouse capacities (supply limits)
    capacity = dict()
    capacity[1] = 50
    capacity[2] = 100
    capacity[3] = 150

    # Regional demands
    demand = dict()
    demand[1] = 25
    demand[2] = 105
    demand[3] = 60
    demand[4] = 30
    demand[5] = 70

    # Cost matrix c[i][j]
    cost = dict()
    # Row 1 (Warehouse 1)
    cost[1, 1] = 10
    cost[1, 2] = 15
    cost[1, 3] = 20
    cost[1, 4] = 20
    cost[1, 5] = 40
    # Row 2 (Warehouse 2)
    cost[2, 1] = 20
    cost[2, 2] = 40
    cost[2, 3] = 15
    cost[2, 4] = 30
    cost[2, 5] = 30
    # Row 3 (Warehouse 3)
    cost[3, 1] = 30
    cost[3, 2] = 35
    cost[3, 3] = 40
    cost[3, 4] = 55
    cost[3, 5] = 25

    # Factory production limit
    factory_limit = 270

    # Decision Variables: x[i, j] = amount shipped from warehouse i to region j
    x = dict()
    for i in warehouses:
        for j in regions:
            x[i, j] = solver.NumVar(0, INF, 'x_%d_%d' % (i, j))

    # Objective Function: Minimize total transportation cost
    total_cost = 0
    for i in warehouses:
        for j in regions:
            total_cost += cost[i, j] * x[i, j]

    solver.Minimize(total_cost)

    # Constraints

    # A. Warehouse Capacity Constraints (Supply Limits)
    for i in warehouses:
        outflow = 0
        for j in regions:
            outflow += x[i, j]
        solver.Add(outflow <= capacity[i])

    # B. Factory Production Constraint (Global Supply Limit)
    total_outflow = 0
    for i in warehouses:
        for j in regions:
            total_outflow += x[i, j]
    solver.Add(total_outflow <= factory_limit)

    # C. Regional Demand Constraints (Equality)
    for j in regions:
        inflow = 0
        for i in warehouses:
            inflow += x[i, j]
        solver.Add(inflow == demand[j])

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()