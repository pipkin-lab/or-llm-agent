from ortools.linear_solver import pywraplp

def solve_goal_programming():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    INF = solver.infinity()

    # Decision variables: x1 (Milk), x2 (Beef), x3 (Eggs)
    x = dict()
    x[1] = solver.NumVar(0, INF, 'x1')
    x[2] = solver.NumVar(0, INF, 'x2')
    x[3] = solver.NumVar(0, INF, 'x3')

    # Deviation variables for Vitamin A
    dA_minus = solver.NumVar(0, INF, 'dA_minus')
    dA_plus = solver.NumVar(0, INF, 'dA_plus')

    # Deviation variables for Vitamin C
    dC_minus = solver.NumVar(0, INF, 'dC_minus')
    dC_plus = solver.NumVar(0, INF, 'dC_plus')

    # Deviation variables for Vitamin D
    dD_minus = solver.NumVar(0, INF, 'dD_minus')
    dD_plus = solver.NumVar(0, INF, 'dD_plus')

    # Deviation variables for Cholesterol
    dchol_minus = solver.NumVar(0, INF, 'dchol_minus')
    dchol_plus = solver.NumVar(0, INF, 'dchol_plus')

    # Deviation variables for Cost
    dcost_minus = solver.NumVar(0, INF, 'dcost_minus')
    dcost_plus = solver.NumVar(0, INF, 'dcost_plus')

    # Parameters
    aA = dict()
    aA[1] = 1
    aA[2] = 1
    aA[3] = 10
    bA = 1

    aC = dict()
    aC[1] = 100
    aC[2] = 10
    aC[3] = 10
    bC = 30

    aD = dict()
    aD[1] = 10
    aD[2] = 100
    aD[3] = 10
    bD = 10

    cchol = dict()
    cchol[1] = 70
    cchol[2] = 50
    cchol[3] = 120
    Tchol = 0

    ccost = dict()
    ccost[1] = 1.5
    ccost[2] = 8
    ccost[3] = 4
    Tcost = 0

    # Constraint 1: Vitamin A goal equation
    solver.Add(aA[1]*x[1] + aA[2]*x[2] + aA[3]*x[3] + dA_minus - dA_plus == bA)

    # Constraint 2: Vitamin C goal equation
    solver.Add(aC[1]*x[1] + aC[2]*x[2] + aC[3]*x[3] + dC_minus - dC_plus == bC)

    # Constraint 3: Vitamin D goal equation
    solver.Add(aD[1]*x[1] + aD[2]*x[2] + aD[3]*x[3] + dD_minus - dD_plus == bD)

    # Constraint 4: Cholesterol goal equation
    solver.Add(cchol[1]*x[1] + cchol[2]*x[2] + cchol[3]*x[3] + dchol_minus - dchol_plus == Tchol)

    # Constraint 5: Cost goal equation
    solver.Add(ccost[1]*x[1] + ccost[2]*x[2] + ccost[3]*x[3] + dcost_minus - dcost_plus == Tcost)

    # Objective: Minimize unwanted deviations
    objective = dA_minus + dC_minus + dD_minus + dchol_plus + dcost_plus
    solver.Minimize(objective)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_goal_programming()