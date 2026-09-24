from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    # Index sets
    G = [1, 2, 3]  # Grades I, II, III
    B = ['R', 'Y', 'Bl']  # Brands Red, Yellow, Blue

    # Parameters
    S = {1: 1500, 2: 2000, 3: 1000}
    C = {1: 6.0, 2: 4.5, 3: 3.0}
    P = {'R': 5.5, 'Y': 5.0, 'Bl': 4.8}
    T_R = 2000
    W = 1000

    # Decision variables
    x = dict()
    for g in G:
        for b in B:
            x[g, b] = solver.NumVar(0, INF, 'x_{}_{}'.format(g, b))

    d_R_minus = solver.NumVar(0, INF, 'd_R_minus')
    d_R_plus = solver.NumVar(0, INF, 'd_R_plus')

    # Supply constraints
    for g in G:
        solver.Add(sum(x[g, b] for b in B) <= S[g])

    # Blending constraints (Hard, Priority 1)
    # Red Brand (R)
    # Grade III < 10%: x[3,'R'] <= 0.10 * (x[1,'R'] + x[2,'R'] + x[3,'R'])
    # 0.90*x[3,'R'] - 0.10*x[1,'R'] - 0.10*x[2,'R'] <= 0
    solver.Add(0.90 * x[3, 'R'] - 0.10 * x[1, 'R'] - 0.10 * x[2, 'R'] <= 0)

    # Grade I > 50%: x[1,'R'] >= 0.50 * (x[1,'R'] + x[2,'R'] + x[3,'R'])
    # 0.50*x[1,'R'] - 0.50*x[2,'R'] - 0.50*x[3,'R'] >= 0
    solver.Add(0.50 * x[1, 'R'] - 0.50 * x[2, 'R'] - 0.50 * x[3, 'R'] >= 0)

    # Yellow Brand (Y)
    # Grade III < 70%: x[3,'Y'] <= 0.70 * (x[1,'Y'] + x[2,'Y'] + x[3,'Y'])
    # 0.30*x[3,'Y'] - 0.70*x[1,'Y'] - 0.70*x[2,'Y'] <= 0
    solver.Add(0.30 * x[3, 'Y'] - 0.70 * x[1, 'Y'] - 0.70 * x[2, 'Y'] <= 0)

    # Grade I > 20%: x[1,'Y'] >= 0.20 * (x[1,'Y'] + x[2,'Y'] + x[3,'Y'])
    # 0.80*x[1,'Y'] - 0.20*x[2,'Y'] - 0.20*x[3,'Y'] >= 0
    solver.Add(0.80 * x[1, 'Y'] - 0.20 * x[2, 'Y'] - 0.20 * x[3, 'Y'] >= 0)

    # Blue Brand (Bl)
    # Grade III < 50%: x[3,'Bl'] <= 0.50 * (x[1,'Bl'] + x[2,'Bl'] + x[3,'Bl'])
    # 0.50*x[3,'Bl'] - 0.50*x[1,'Bl'] - 0.50*x[2,'Bl'] <= 0
    solver.Add(0.50 * x[3, 'Bl'] - 0.50 * x[1, 'Bl'] - 0.50 * x[2, 'Bl'] <= 0)

    # Grade I > 10%: x[1,'Bl'] >= 0.10 * (x[1,'Bl'] + x[2,'Bl'] + x[3,'Bl'])
    # 0.90*x[1,'Bl'] - 0.10*x[2,'Bl'] - 0.10*x[3,'Bl'] >= 0
    solver.Add(0.90 * x[1, 'Bl'] - 0.10 * x[2, 'Bl'] - 0.10 * x[3, 'Bl'] >= 0)

    # Red Production Goal (Priority 3)
    # (x[1,'R'] + x[2,'R'] + x[3,'R']) + d_R_minus - d_R_plus = 2000
    solver.Add(x[1, 'R'] + x[2, 'R'] + x[3, 'R'] + d_R_minus - d_R_plus == T_R)

    # Objective Function
    # Profit = sum_b P[b] * sum_g x[g,b] - sum_g C[g] * sum_b x[g,b]
    # Minimize Z = -W * Profit + d_R_minus

    profit_terms = []
    for b in B:
        for g in G:
            profit_terms.append(P[b] * x[g, b] - C[g] * x[g, b])

    profit_expr = sum(profit_terms)
    objective = -W * profit_expr + d_R_minus

    solver.Minimize(objective)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()