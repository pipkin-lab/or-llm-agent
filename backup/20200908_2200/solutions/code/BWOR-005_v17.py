from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Sets
    cargo_types = ['A', 'B', 'C']
    compartments = ['F', 'M', 'R']

    # Parameters
    Q = {'A': 600, 'B': 1000, 'C': 800}
    v = {'A': 10, 'B': 5, 'C': 7}
    w = {'A': 8, 'B': 6, 'C': 4}
    r = {'A': 1000, 'B': 700, 'C': 600}

    W_max = {'F': 2000, 'M': 3000, 'R': 1500}
    V_max = {'F': 4000, 'M': 5000, 'R': 1500}

    # Balance parameters
    # rho_FM = 2/3, delta_FM = 0.15 -> [2/3 * 0.85, 2/3 * 1.15] = [0.566667, 0.766667]
    # rho_RM = 1/2, delta_RM = 0.15 -> [1/2 * 0.85, 1/2 * 1.15] = [0.425, 0.575]
    # rho_FR = 4/3, delta_FR = 0.10 -> [4/3 * 0.9, 4/3 * 1.1] = [1.2, 1.466667]

    # Variables
    x = dict()
    for c in cargo_types:
        for k in compartments:
            x[c, k] = solver.IntVar(0, inf, 'x_' + c + '_' + k)

    # Objective
    obj_terms = []
    for c in cargo_types:
        for k in compartments:
            obj_terms.append(r[c] * x[c, k])
    objective = sum(obj_terms)
    solver.Maximize(objective)

    # A. Supply Constraints
    for c in cargo_types:
        solver.Add(sum(x[c, k] for k in compartments) <= Q[c])

    # B. Volume Constraints
    for k in compartments:
        solver.Add(sum(v[c] * x[c, k] for c in cargo_types) <= V_max[k])

    # C. Weight Capacity Constraints
    for k in compartments:
        solver.Add(sum(w[c] * x[c, k] for c in cargo_types) <= W_max[k])

    # Helper to get weight expression for a compartment
    def weight_expr(k):
        return sum(w[c] * x[c, k] for c in cargo_types)

    WF = weight_expr('F')
    WM = weight_expr('M')
    WR = weight_expr('R')

    # D. Balance Constraints

    # D1: Front vs Middle
    # 1. WF - 0.766667 * WM <= 0
    solver.Add(WF - (2.0/3.0 * 1.15) * WM <= 0)
    # 2. 0.566667 * WM - WF <= 0
    solver.Add((2.0/3.0 * 0.85) * WM - WF <= 0)

    # D2: Rear vs Middle
    # 1. WR - 0.575 * WM <= 0
    solver.Add(WR - (0.5 * 1.15) * WM <= 0)
    # 2. 0.425 * WM - WR <= 0
    solver.Add((0.5 * 0.85) * WM - WR <= 0)

    # D3: Front vs Rear
    # 1. WF - 1.466667 * WR <= 0
    solver.Add(WF - (4.0/3.0 * 1.10) * WR <= 0)
    # 2. 1.2 * WR - WF <= 0
    solver.Add((4.0/3.0 * 0.90) * WR - WF <= 0)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()