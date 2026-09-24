from ortools.linear_solver import pywraplp

def solve_production_inventory_problem():
    # Problem parameters
    T = 4
    demand = {1: 15, 2: 20, 3: 25, 4: 20}
    capacity = {1: 25, 2: 35, 3: 30, 4: 20}
    production_cost = {1: 12.0, 2: 11.0, 3: 11.5, 4: 12.5}
    holding_cost = 0.1

    # Create LP solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    # Decision variables: x[t, s] for 1 <= t <= s <= 4
    x = dict()
    for t in range(1, T + 1):
        for s in range(t, T + 1):
            x[t, s] = solver.NumVar(0, INF, 'x_{}_{}'.format(t, s))

    # Objective function: minimize total cost
    objective_terms = []
    for t in range(1, T + 1):
        for s in range(t, T + 1):
            cost = production_cost[t] + holding_cost * (s - t)
            objective_terms.append(cost * x[t, s])

    objective = sum(objective_terms)
    solver.Minimize(objective)

    # Demand satisfaction constraints
    for s in range(1, T + 1):
        demand_expr = sum(x[t, s] for t in range(1, s + 1))
        solver.Add(demand_expr == demand[s])

    # Production capacity constraints
    for t in range(1, T + 1):
        production_expr = sum(x[t, s] for s in range(t, T + 1))
        solver.Add(production_expr <= capacity[t])

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_inventory_problem()