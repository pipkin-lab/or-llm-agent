from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    # Decision variables
    x1 = solver.NumVar(0, INF, 'x1')  # Soybeans (hm²)
    x2 = solver.NumVar(0, INF, 'x2')  # Corn (hm²)
    x3 = solver.NumVar(0, INF, 'x3')  # Wheat (hm²)
    y1 = solver.NumVar(0, INF, 'y1')  # Cows
    y2 = solver.NumVar(0, INF, 'y2')  # Chickens
    z_aw = solver.NumVar(0, INF, 'z_aw')  # Labor sent out AW
    z_ss = solver.NumVar(0, INF, 'z_ss')  # Labor sent out SS

    # Objective: Maximize total net income
    objective = (
        175 * x1 + 300 * x2 + 120 * x3
        + 400 * y1 + 2 * y2
        + 1.8 * z_aw + 2.1 * z_ss
    )
    solver.Maximize(objective)

    # Land constraint
    solver.Add(x1 + x2 + x3 + 1.5 * y1 <= 100)

    # Fund constraint
    solver.Add(400 * y1 + 3 * y2 <= 15000)

    # Labor constraint (Autumn/Winter)
    solver.Add(20 * x1 + 35 * x2 + 10 * x3 + 100 * y1 + 0.6 * y2 + z_aw <= 3500)

    # Labor constraint (Spring/Summer)
    solver.Add(50 * x1 + 75 * x2 + 40 * x3 + 50 * y1 + 0.3 * y2 + z_ss <= 4000)

    # Capacity constraints
    solver.Add(y1 <= 32)
    solver.Add(y2 <= 3000)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()