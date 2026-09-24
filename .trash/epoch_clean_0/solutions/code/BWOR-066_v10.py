from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Parameters
    S = dict()
    P = dict()
    S[1] = 10
    S[2] = 9
    S[3] = 11
    S[4] = 15
    P[1] = 12
    P[2] = 9
    P[3] = 13
    P[4] = 17
    Wmax = 1000
    I0 = 500

    # Decision variables
    x = dict()
    y = dict()
    I = dict()
    for t in range(1, 5):
        x[t] = solver.IntVar(0, inf, 'x_' + str(t))
        y[t] = solver.IntVar(0, inf, 'y_' + str(t))
        I[t] = solver.IntVar(0, Wmax, 'I_' + str(t))

    # Objective: Maximize total profit
    obj_terms = []
    for t in range(1, 5):
        obj_terms.append(P[t] * y[t] - S[t] * x[t])
    solver.Maximize(sum(obj_terms))

    # Inventory balance constraints
    # Month 1: I1 = I0 - y1 + x1
    solver.Add(I[1] == I0 - y[1] + x[1])
    # Month 2: I2 = I1 - y2 + x2
    solver.Add(I[2] == I[1] - y[2] + x[2])
    # Month 3: I3 = I2 - y3 + x3
    solver.Add(I[3] == I[2] - y[3] + x[3])
    # Month 4: I4 = I3 - y4 + x4
    solver.Add(I[4] == I[3] - y[4] + x[4])

    # Sales availability constraints
    solver.Add(y[1] <= I0)
    solver.Add(y[2] <= I[1])
    solver.Add(y[3] <= I[2])
    solver.Add(y[4] <= I[3])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()