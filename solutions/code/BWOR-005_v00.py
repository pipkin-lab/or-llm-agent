from ortools.linear_solver import pywraplp

def solve_cargo_loading():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    cargo_types = ['A', 'B', 'C']
    compartments = ['F', 'M', 'R']

    # Decision variables: x[i][j] integer >= 0
    x = dict()
    for i in cargo_types:
        for j in compartments:
            x[i, j] = solver.IntVar(0, inf, 'x_' + i + '_' + j)

    # Parameters
    r = {'A': 1000, 'B': 700, 'C': 600}
    v = {'A': 10, 'B': 5, 'C': 7}
    w = {'A': 8, 'B': 6, 'C': 4}
    V_cap = {'F': 4000, 'M': 5000, 'R': 1500}
    W_cap = {'F': 2000, 'M': 3000, 'R': 1500}
    supply = {'A': 600, 'B': 1000, 'C': 800}

    # Objective: Maximize total revenue
    obj = 0
    for i in cargo_types:
        for j in compartments:
            obj += r[i] * x[i, j]
    solver.Maximize(obj)

    # A. Cargo Supply Constraints
    for i in cargo_types:
        solver.Add(sum(x[i, j] for j in compartments) <= supply[i])

    # B. Volume Constraints
    for j in compartments:
        solver.Add(sum(v[i] * x[i, j] for i in cargo_types) <= V_cap[j])

    # C. Weight (Load) Constraints
    for j in compartments:
        solver.Add(sum(w[i] * x[i, j] for i in cargo_types) <= W_cap[j])

    # D. Balance (Stability) Constraints
    # Define actual weight expressions
    WF = sum(w[i] * x[i, 'F'] for i in cargo_types)
    WM = sum(w[i] * x[i, 'M'] for i in cargo_types)
    WR = sum(w[i] * x[i, 'R'] for i in cargo_types)

    # 1. Front vs Middle: 0.5667 <= WF/WM <= 0.7667
    # WF - 0.7667*WM <= 0
    solver.Add(WF - 0.7667 * WM <= 0)
    # -WF + 0.5667*WM <= 0
    solver.Add(-WF + 0.5667 * WM <= 0)

    # 2. Rear vs Middle: 0.425 <= WR/WM <= 0.575
    # WR - 0.575*WM <= 0
    solver.Add(WR - 0.575 * WM <= 0)
    # -WR + 0.425*WM <= 0
    solver.Add(-WR + 0.425 * WM <= 0)

    # 3. Front vs Rear: 1.2 <= WF/WR <= 1.4667
    # WF - 1.4667*WR <= 0
    solver.Add(WF - 1.4667 * WR <= 0)
    # -WF + 1.2*WR <= 0
    solver.Add(-WF + 1.2 * WR <= 0)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_cargo_loading()