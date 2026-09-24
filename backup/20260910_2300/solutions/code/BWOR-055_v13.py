from ortools.linear_solver import pywraplp

def solve_production_milp():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print("NO_FEASIBLE_SOLUTION")
        return

    # Index set: i in {1, 2, 3}
    indices = [1, 2, 3]

    # Parameters
    a = dict()
    a[1] = 3
    a[2] = 2
    a[3] = 6

    b = dict()
    b[1] = 4
    b[2] = 3
    b[3] = 6

    p = dict()
    p[1] = 120
    p[2] = 80
    p[3] = 180

    c = dict()
    c[1] = 60
    c[2] = 40
    c[3] = 80

    f = dict()
    f[1] = 2000
    f[2] = 1500
    f[3] = 1000

    m = dict()
    m[1] = p[1] - c[1]
    m[2] = p[2] - c[2]
    m[3] = p[3] - c[3]

    A = 150
    B = 160

    M = dict()
    M[1] = 40
    M[2] = 53
    M[3] = 25

    # Decision variables
    x = dict()
    y = dict()

    for i in indices:
        x[i] = solver.NumVar(0, solver.infinity(), 'x_' + str(i))
        y[i] = solver.BoolVar('y_' + str(i))

    # Objective: Maximize total profit
    objective_terms = []
    for i in indices:
        objective_terms.append(m[i] * x[i])
        objective_terms.append(-f[i] * y[i])

    solver.Maximize(sum(objective_terms))

    # Resource constraints
    labor_terms = []
    material_terms = []
    for i in indices:
        labor_terms.append(a[i] * x[i])
        material_terms.append(b[i] * x[i])

    solver.Add(sum(labor_terms) <= A)
    solver.Add(sum(material_terms) <= B)

    # Big-M linking constraints
    for i in indices:
        solver.Add(x[i] <= M[i] * y[i])

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_milp()