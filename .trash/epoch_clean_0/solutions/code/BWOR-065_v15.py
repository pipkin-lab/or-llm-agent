from ortools.linear_solver import pywraplp

def solve_production_inventory():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Index set: months 1 through 6
    T = [1, 2, 3, 4, 5, 6]

    # Parameters
    d = dict()
    d[1] = 1
    d[2] = 2
    d[3] = 5
    d[4] = 3
    d[5] = 2
    d[6] = 1

    C = 4
    W = 3
    c_v = 10
    c_f = 4
    h = 1

    # Decision variables
    x = dict()
    I = dict()
    y = dict()

    for t in T:
        x[t] = solver.NumVar(0, inf, 'x_' + str(t))
        I[t] = solver.NumVar(0, inf, 'I_' + str(t))
        y[t] = solver.BoolVar('y_' + str(t))

    # Objective: minimize total cost
    obj_terms = []
    for t in T:
        obj_terms.append(c_v * x[t] + c_f * y[t] + h * I[t])
    solver.Minimize(sum(obj_terms))

    # Inventory balance constraints
    # I_0 = 0
    for t in T:
        if t == 1:
            # I_0 + x_1 - d_1 = I_1  =>  0 + x_1 - d_1 = I_1
            solver.Add(x[1] - d[1] == I[1])
        else:
            # I_{t-1} + x_t - d_t = I_t
            solver.Add(I[t - 1] + x[t] - d[t] == I[t])

    # Zero final inventory
    solver.Add(I[6] == 0)

    # Production capacity: x_t <= C * y_t
    for t in T:
        solver.Add(x[t] <= C * y[t])

    # Storage capacity: I_t <= W for t = 1..5 (I_6 = 0 already)
    for t in [1, 2, 3, 4, 5]:
        solver.Add(I[t] <= W)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_inventory()