from ortools.linear_solver import pywraplp

def solve_set_covering_milp(c1, c2, c3, c4):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        raise ValueError("Unable to create SCIP solver")

    # Index sets
    customers = ['A', 'B', 'C', 'D', 'E']
    trucks = [1, 2, 3, 4]

    # Parameters
    d = dict()
    d['A'] = 1
    d['B'] = 2
    d['C'] = 3
    d['D'] = 4
    d['E'] = 8

    K = dict()
    K[1] = 2
    K[2] = 6
    K[3] = 8
    K[4] = 11

    c = dict()
    c[1] = c1
    c[2] = c2
    c[3] = c3
    c[4] = c4

    # Variables
    y = dict()
    for i in customers:
        for j in trucks:
            y[i, j] = solver.BoolVar('y_' + i + '_' + str(j))

    z = dict()
    for j in trucks:
        z[j] = solver.BoolVar('z_' + str(j))

    # Objective: minimize sum c_j * z_j
    obj_terms = []
    for j in trucks:
        obj_terms.append(c[j] * z[j])
    solver.Minimize(sum(obj_terms))

    # Constraint 1: Each customer assigned to exactly one truck
    for i in customers:
        solver.Add(sum(y[i, j] for j in trucks) == 1)

    # Constraint 2: Truck capacity
    for j in trucks:
        solver.Add(sum(d[i] * y[i, j] for i in customers) <= K[j])

    # Constraint 3: Linking constraint (if truck used, serves at least one; if serves, used)
    for j in trucks:
        solver.Add(sum(y[i, j] for i in customers) <= 5 * z[j])

    # Constraint 4: Conflict A and C
    for j in trucks:
        solver.Add(y['A', j] + y['C', j] <= 1)

    # Constraint 5: Conflict B and D
    for j in trucks:
        solver.Add(y['B', j] + y['D', j] <= 1)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

# Since costs c1..c4 are not numerically provided, we cannot run with specific values.
# Per instructions: raise ValueError if parameters are not provided.
# However, the function is defined to accept them. To make the script executable
# and demonstrate the model, we raise an error indicating missing parameters.
raise ValueError("Parameters c_1, c_2, c_3, c_4 not provided in model. Please supply truck usage costs to solve the MILP.")