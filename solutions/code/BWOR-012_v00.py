from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    grades = ['I', 'II', 'III']
    brands = ['R', 'Y', 'B']

    x = dict()
    for i in grades:
        for j in brands:
            x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

    # Supply constraints
    solver.Add(x['I', 'R'] + x['I', 'Y'] + x['I', 'B'] <= 1500)
    solver.Add(x['II', 'R'] + x['II', 'Y'] + x['II', 'B'] <= 2000)
    solver.Add(x['III', 'R'] + x['III', 'Y'] + x['III', 'B'] <= 1000)

    # Blending ratio constraints (linearized)
    # Red: Grade III < 10% -> 0.1*x_I + 0.1*x_II - 0.9*x_III >= 0
    solver.Add(0.1 * x['I', 'R'] + 0.1 * x['II', 'R'] - 0.9 * x['III', 'R'] >= 0)
    # Red: Grade I > 50% -> 0.5*x_I - 0.5*x_II - 0.5*x_III >= 0
    solver.Add(0.5 * x['I', 'R'] - 0.5 * x['II', 'R'] - 0.5 * x['III', 'R'] >= 0)

    # Yellow: Grade III < 70% -> 0.7*x_I + 0.7*x_II - 0.3*x_III >= 0
    solver.Add(0.7 * x['I', 'Y'] + 0.7 * x['II', 'Y'] - 0.3 * x['III', 'Y'] >= 0)
    # Yellow: Grade I > 20% -> 0.8*x_I - 0.2*x_II - 0.2*x_III >= 0
    solver.Add(0.8 * x['I', 'Y'] - 0.2 * x['II', 'Y'] - 0.2 * x['III', 'Y'] >= 0)

    # Blue: Grade III < 50% -> 0.5*x_I + 0.5*x_II - 0.5*x_III >= 0
    solver.Add(0.5 * x['I', 'B'] + 0.5 * x['II', 'B'] - 0.5 * x['III', 'B'] >= 0)
    # Blue: Grade I > 10% -> 0.9*x_I - 0.1*x_II - 0.1*x_III >= 0
    solver.Add(0.9 * x['I', 'B'] - 0.1 * x['II', 'B'] - 0.1 * x['III', 'B'] >= 0)

    # Production quantity constraints
    # Red minimum production: P_R >= 2000
    solver.Add(x['I', 'R'] + x['II', 'R'] + x['III', 'R'] >= 2000)

    # Objective: Maximize Profit
    # Z = sum over i,j of (Price_j - Cost_i) * x_ij
    price = {'R': 5.5, 'Y': 5.0, 'B': 4.8}
    cost = {'I': 6.0, 'II': 4.5, 'III': 3.0}

    obj = 0
    for i in grades:
        for j in brands:
            obj += (price[j] - cost[i]) * x[i, j]

    solver.Maximize(obj)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()