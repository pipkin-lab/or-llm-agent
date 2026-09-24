from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("No solver available")
        return

    INF = solver.infinity()

    # Decision variables
    x_A = solver.NumVar(0, INF, 'x_A')
    x_B = solver.NumVar(0, INF, 'x_B')
    x_C = solver.NumVar(0, INF, 'x_C')

    # Parameters
    F = 1000
    Reserve = 100
    V = F - Reserve  # 900
    r_A = 0.05
    r_B = 0.07
    r_C = 0.10
    Min_A = 300
    MaxShare = 0.35 * F  # 350

    # Objective: Maximize total profit
    objective = r_A * x_A + r_B * x_B + r_C * x_C
    solver.Maximize(objective)

    # Constraint 1: Total investment limit
    solver.Add(x_A + x_B + x_C <= V)

    # Constraint 2: Minimum investment in Product A
    solver.Add(x_A >= Min_A)

    # Constraint 3: Max share per product (35% of total fund)
    solver.Add(x_A <= MaxShare)
    solver.Add(x_B <= MaxShare)
    solver.Add(x_C <= MaxShare)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()