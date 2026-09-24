from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("No solution found")
        return None

    # Plants and Regions
    plants = ['A', 'B', 'C', 'D']
    regions = ['I', 'II', 'III', 'IV', 'V', 'VI']

    # Supply capacities (tons)
    S = dict()
    S['A'] = 200
    S['B'] = 300
    S['C'] = 400
    S['D'] = 100

    # Demand (tons)
    D = dict()
    D['I'] = 200
    D['II'] = 150
    D['III'] = 400
    D['IV'] = 100
    D['V'] = 150
    D['VI'] = 150

    # Production cost per kg (yuan/kg)
    c_p = dict()
    c_p['A'] = 1.2
    c_p['B'] = 1.4
    c_p['C'] = 1.1
    c_p['D'] = 1.5

    # Sales price per kg (yuan/kg)
    v_r = dict()
    v_r['I'] = 2.0
    v_r['II'] = 2.4
    v_r['III'] = 1.8
    v_r['IV'] = 2.2
    v_r['V'] = 1.6
    v_r['VI'] = 2.0

    # Transportation cost per kg (yuan/kg)
    # t[p][r]
    t = dict()
    t['A'] = dict()
    t['B'] = dict()
    t['C'] = dict()
    t['D'] = dict()
    
    t['A']['I'] = 0.5
    t['A']['II'] = 0.4
    t['A']['III'] = 0.3
    t['A']['IV'] = 0.4
    t['A']['V'] = 0.3
    t['A']['VI'] = 0.1

    t['B']['I'] = 0.3
    t['B']['II'] = 0.8
    t['B']['III'] = 0.9
    t['B']['IV'] = 0.5
    t['B']['V'] = 0.6
    t['B']['VI'] = 0.2

    t['C']['I'] = 0.7
    t['C']['II'] = 0.7
    t['C']['III'] = 0.3
    t['C']['IV'] = 0.7
    t['C']['V'] = 0.4
    t['C']['VI'] = 0.4

    t['D']['I'] = 0.6
    t['D']['II'] = 0.4
    t['D']['III'] = 0.2
    t['D']['IV'] = 0.6
    t['D']['V'] = 0.5
    t['D']['VI'] = 0.8

    # Decision Variables: x[p][r] in tons
    x = dict()
    for p in plants:
        x[p] = dict()
        for r in regions:
            x[p][r] = solver.NumVar(0, solver.infinity(), 'x_' + p + '_' + r)

    # Objective Function
    # Maximize total profit: sum(1000 * (v_r - c_p - t_p_r) * x_p_r)
    objective = 0
    for p in plants:
        for r in regions:
            profit_per_kg = v_r[r] - c_p[p] - t[p][r]
            profit_per_ton = 1000 * profit_per_kg
            objective += profit_per_ton * x[p][r]

    solver.Maximize(objective)

    # Constraints

    # 1. Supply Constraints (Plant Capacities)
    for p in plants:
        solver.Add(sum(x[p][r] for r in regions) <= S[p])

    # 2. Demand Constraints (Region Limits)
    for r in regions:
        if r == 'IV':
            # Region IV must be fully satisfied
            solver.Add(sum(x[p][r] for p in plants) == D[r])
        else:
            # Other regions cannot exceed demand
            solver.Add(sum(x[p][r] for p in plants) <= D[r])

    # 3. Specific Constraint: Region III at least 100 tons
    solver.Add(sum(x[p]['III'] for p in plants) >= 100)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()