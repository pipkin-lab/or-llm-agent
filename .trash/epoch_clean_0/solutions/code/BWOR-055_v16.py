from ortools.linear_solver import pywraplp

def solve_production_milp():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Could not create solver")
        return

    # Parameter definitions
    products = [1, 2, 3]  # 1: Shirt, 2: T-shirt, 3: Casual Wear
    price = dict()
    var_cost = dict()
    labor = dict()
    material = dict()
    fixed_cost = dict()
    upper_bound = dict()

    price[1] = 120
    price[2] = 80
    price[3] = 180

    var_cost[1] = 60
    var_cost[2] = 40
    var_cost[3] = 80

    labor[1] = 3
    labor[2] = 2
    labor[3] = 6

    material[1] = 4
    material[2] = 3
    material[3] = 6

    fixed_cost[1] = 2000
    fixed_cost[2] = 1500
    fixed_cost[3] = 1000

    upper_bound[1] = 40
    upper_bound[2] = 53
    upper_bound[3] = 25

    labor_max = 150
    material_max = 160

    # Decision variables
    x = dict()
    y = dict()
    for i in products:
        x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))
        y[i] = solver.BoolVar('y_' + str(i))

    # Objective function: Maximize profit
    obj = 0
    for i in products:
        obj += (price[i] - var_cost[i]) * x[i]
    for i in products:
        obj -= fixed_cost[i] * y[i]

    solver.Maximize(obj)

    # Labor constraint
    labor_expr = 0
    for i in products:
        labor_expr += labor[i] * x[i]
    solver.Add(labor_expr <= labor_max)

    # Material constraint
    material_expr = 0
    for i in products:
        material_expr += material[i] * x[i]
    solver.Add(material_expr <= material_max)

    # Linking constraints
    for i in products:
        solver.Add(x[i] <= upper_bound[i] * y[i])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_milp()