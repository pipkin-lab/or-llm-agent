from ortools.linear_solver import pywraplp

def solve_cargo_loading():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index sets
    K = ['A', 'B', 'C']
    C = ['F', 'M', 'R']

    # Parameters
    CapLoad = dict()
    CapLoad['F'] = 2000
    CapLoad['M'] = 3000
    CapLoad['R'] = 1500

    CapVol = dict()
    CapVol['F'] = 4000
    CapVol['M'] = 5000
    CapVol['R'] = 1500

    Qty = dict()
    Qty['A'] = 600
    Qty['B'] = 1000
    Qty['C'] = 800

    Vol = dict()
    Vol['A'] = 10
    Vol['B'] = 5
    Vol['C'] = 7

    Wt = dict()
    Wt['A'] = 8
    Wt['B'] = 6
    Wt['C'] = 4

    Price = dict()
    Price['A'] = 1000
    Price['B'] = 700
    Price['C'] = 600

    # Decision variables: x[k, c] = number of pieces of cargo k in compartment c
    x = dict()
    for k in K:
        for c in C:
            x[k, c] = solver.IntVar(0, INF, 'x_' + k + '_' + c)

    # Objective: Maximize total revenue
    obj_terms = []
    for k in K:
        for c in C:
            obj_terms.append(Price[k] * x[k, c])
    solver.Maximize(sum(obj_terms))

    # Supply constraints
    for k in K:
        solver.Add(sum(x[k, c] for c in C) <= Qty[k])

    # Volume capacity constraints
    for c in C:
        solver.Add(sum(Vol[k] * x[k, c] for k in K) <= CapVol[c])

    # Weight capacity constraints
    for c in C:
        solver.Add(sum(Wt[k] * x[k, c] for k in K) <= CapLoad[c])

    # Define weight expressions for each compartment
    WF = sum(Wt[k] * x[k, 'F'] for k in K)
    WM = sum(Wt[k] * x[k, 'M'] for k in K)
    WR = sum(Wt[k] * x[k, 'R'] for k in K)

    # Maritime Safety Balance Constraints

    # Front/Middle Deviation <= 15%
    # 30*WF - 17*WM >= 0
    solver.Add(30 * WF - 17 * WM >= 0)
    # 30*WF - 23*WM <= 0
    solver.Add(30 * WF - 23 * WM <= 0)

    # Rear/Middle Deviation <= 15%
    # 40*WR - 17*WM >= 0
    solver.Add(40 * WR - 17 * WM >= 0)
    # 40*WR - 23*WM <= 0
    solver.Add(40 * WR - 23 * WM <= 0)

    # Front/Rear Deviation <= 10%
    # 5*WF - 6*WR >= 0
    solver.Add(5 * WF - 6 * WR >= 0)
    # 15*WF - 22*WR <= 0
    solver.Add(15 * WF - 22 * WR <= 0)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_cargo_loading()