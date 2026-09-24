from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Sets
    T = range(1, 7)  # t = 1..6
    P = range(1, 8)  # j = 1..7
    M = range(1, 6)  # m = 1..5 (G, UD, HD, B, Pl)

    # Parameters
    # a[m][j]: machine hours per unit
    # m indices: 0=G, 1=UD, 2=HD, 3=B, 4=Pl
    # j indices: 0..6 for products I..VII
    a = [
        [0.5, 0.7, 0, 0, 0.3, 0.2, 0.5],  # G
        [0.1, 0.2, 0, 0.3, 0, 0.6, 0],     # UD
        [0.2, 0, 0.8, 0, 0, 0, 0.6],       # HD
        [0.05, 0.03, 0, 0.07, 0.1, 0, 0.08], # B
        [0, 0, 0.01, 0, 0.05, 0, 0.05]      # Pl
    ]

    c = [100, 60, 80, 40, 110, 90, 30]

    # D[t][j]: demand, t=0..5 for Jan..Jun
    D = [
        [500, 1000, 300, 300, 800, 200, 100],   # Jan
        [600, 500, 200, 0, 400, 300, 150],      # Feb
        [300, 600, 0, 0, 500, 400, 100],        # Mar
        [200, 300, 400, 500, 200, 0, 100],      # Apr
        [0, 100, 500, 100, 1000, 300, 0],       # May
        [500, 500, 100, 300, 1100, 500, 60]     # Jun
    ]

    h = 5  # holding cost per unit per month
    I_max = 100
    I_0 = [0] * 7
    I_T = 50

    # Machine counts and maintenance
    N_m = [4, 2, 3, 1, 1]  # G, UD, HD, B, Pl
    # K[t][m]: machines in maintenance, t=0..5
    K = [
        [1, 0, 0, 0, 0],  # Jan: G=1
        [0, 0, 2, 0, 0],  # Feb: HD=2
        [0, 0, 0, 1, 0],  # Mar: B=1
        [0, 1, 0, 0, 0],  # Apr: UD=1
        [1, 1, 0, 0, 0],  # May: G=1, UD=1
        [0, 0, 1, 0, 1]   # Jun: HD=1, Pl=1
    ]

    # Capacity per machine per month = 384
    hours_per_machine = 384
    Cap = {}
    for t in range(6):
        for m in range(5):
            Cap[t, m] = (N_m[m] - K[t][m]) * hours_per_machine

    # Decision variables
    x = dict()
    S = dict()
    Inv = dict()

    for t in T:
        for j in P:
            x[t, j] = solver.NumVar(0, inf, 'x_' + str(t) + '_' + str(j))
            S[t, j] = solver.NumVar(0, inf, 'S_' + str(t) + '_' + str(j))
            Inv[t, j] = solver.NumVar(0, inf, 'Inv_' + str(t) + '_' + str(j))

    # Objective
    obj = 0
    for t in T:
        for j in P:
            obj += c[j - 1] * S[t, j]
            obj -= h * Inv[t, j]
    solver.Maximize(obj)

    # 1. Inventory balance
    for t in T:
        for j in P:
            if t == 1:
                # Inv_0,j = 0
                solver.Add(x[t, j] - S[t, j] == Inv[t, j])
            else:
                solver.Add(Inv[t - 1, j] + x[t, j] - S[t, j] == Inv[t, j])

    # 2. Sales demand constraint
    for t in T:
        for j in P:
            solver.Add(S[t, j] <= D[t - 1][j - 1])

    # 3. Inventory capacity constraint
    for t in T:
        for j in P:
            solver.Add(Inv[t, j] <= I_max)

    # 4. Final inventory requirement
    for j in P:
        solver.Add(Inv[6, j] == I_T)

    # 5. Machine capacity constraints
    for t in T:
        for m in M:
            cap_expr = 0
            for j in P:
                cap_expr += a[m - 1][j - 1] * x[t, j]
            solver.Add(cap_expr <= Cap[t - 1, m - 1])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()