from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    plants = ['A', 'B', 'C', 'D']
    regions = ['I', 'II', 'III', 'IV', 'V', 'VI']

    supply = dict()
    supply['A'] = 200
    supply['B'] = 300
    supply['C'] = 400
    supply['D'] = 100

    demand = dict()
    demand['I'] = 200
    demand['II'] = 150
    demand['III'] = 400
    demand['IV'] = 100
    demand['V'] = 150
    demand['VI'] = 150

    profit = dict()
    profit['A', 'I'] = 300
    profit['A', 'II'] = 800
    profit['A', 'III'] = 300
    profit['A', 'IV'] = 600
    profit['A', 'V'] = 100
    profit['A', 'VI'] = 700
    profit['B', 'I'] = 300
    profit['B', 'II'] = 200
    profit['B', 'III'] = -500
    profit['B', 'IV'] = 300
    profit['B', 'V'] = -400
    profit['B', 'VI'] = 400
    profit['C', 'I'] = 200
    profit['C', 'II'] = 600
    profit['C', 'III'] = 400
    profit['C', 'IV'] = 400
    profit['C', 'V'] = 100
    profit['C', 'VI'] = 500
    profit['D', 'I'] = -100
    profit['D', 'II'] = 500
    profit['D', 'III'] = 100
    profit['D', 'IV'] = 100
    profit['D', 'V'] = -400
    profit['D', 'VI'] = -300

    x = dict()
    for i in plants:
        for j in regions:
            x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

    # Supply constraints
    for i in plants:
        solver.Add(sum(x[i, j] for j in regions) <= supply[i])

    # Demand constraints
    for j in regions:
        if j == 'IV':
            solver.Add(sum(x[i, j] for i in plants) == demand[j])
        elif j == 'III':
            solver.Add(sum(x[i, j] for i in plants) <= demand[j])
            solver.Add(sum(x[i, j] for i in plants) >= 100)
        else:
            solver.Add(sum(x[i, j] for i in plants) <= demand[j])

    # Objective
    obj_terms = []
    for i in plants:
        for j in regions:
            obj_terms.append(profit[i, j] * x[i, j])
    solver.Maximize(sum(obj_terms))

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()