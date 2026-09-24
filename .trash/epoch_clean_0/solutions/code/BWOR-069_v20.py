from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Parameters
    W = 10
    weights = dict()
    weights[1] = 2
    weights[2] = 3
    weights[3] = 4

    profits = dict()
    profits[1] = 100
    profits[2] = 140
    profits[3] = 180

    products = [1, 2, 3]

    # Decision variables: x_i >= 0 integer
    x = dict()
    for i in products:
        x[i] = solver.IntVar(0, INF, 'x_' + str(i))

    # Objective: maximize total profit
    obj_terms = []
    for i in products:
        obj_terms.append(profits[i] * x[i])
    obj = sum(obj_terms)
    solver.Maximize(obj)

    # Constraint: total weight <= capacity
    weight_terms = []
    for i in products:
        weight_terms.append(weights[i] * x[i])
    solver.Add(sum(weight_terms) <= W)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()