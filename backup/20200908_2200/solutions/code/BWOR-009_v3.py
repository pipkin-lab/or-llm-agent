from ortools.linear_solver import pywraplp

def solve_production_problem():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("No solver found")
        return

    # Parameters
    quarters = [1, 2, 3, 4]
    C = {1: 25, 2: 35, 3: 30, 4: 20}
    D = {1: 15, 2: 20, 3: 25, 4: 20}
    p = {1: 12.0, 2: 11.0, 3: 11.5, 4: 12.5}
    h = 0.1

    # Decision variables: x[i, t] for i <= t
    x = {}
    for i in quarters:
        for t in quarters:
            if t >= i:
                x[i, t] = solver.NumVar(0, solver.infinity(), f'x_{i}_{t}')

    # Objective function
    objective = 0
    for i in quarters:
        for t in quarters:
            if t >= i:
                cost = p[i] + h * (t - i)
                objective += cost * x[i, t]

    solver.Minimize(objective)

    # Production capacity constraints
    for i in quarters:
        total_production = 0
        for t in quarters:
            if t >= i:
                total_production += x[i, t]
        solver.Add(total_production <= C[i])

    # Delivery demand constraints
    for t in quarters:
        total_delivery = 0
        for i in quarters:
            if i <= t:
                total_delivery += x[i, t]
        solver.Add(total_delivery == D[t])

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
        # Optional: print variable values for verification
        for i in quarters:
            for t in quarters:
                if t >= i:
                    print(f"x_{i}_{t} = {x[i, t].solution_value()}")
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == "__main__":
    solve_production_problem()