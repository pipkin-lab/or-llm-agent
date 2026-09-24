from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Parameters
    a = [30, 30, 30]
    b = [10.0 / 3.0, 40.0 / 3.0, 80.0 / 3.0]
    c = [2, 3, 1]
    W_fixed = 100
    M_avail = 30000
    w_temp_cost = 40

    # Indices (1-indexed as per model)
    P = [1, 2, 3]

    # Decision Variables
    x = dict()
    for p in P:
        x[p] = solver.NumVar(0, INF, 'x_' + str(p))

    N_temp = solver.IntVar(0, INF, 'N_temp')

    # Objective: Maximize Z = sum(c_p * x_p) - w_temp_cost * N_temp
    obj_terms = [c[p - 1] * x[p] for p in P]
    obj_terms.append(-w_temp_cost * N_temp)
    objective = sum(obj_terms)
    solver.Maximize(objective)

    # Constraint A: Labor Capacity
    # sum(x_p) <= 30 * (W_fixed + N_temp)
    labor_lhs = sum(x[p] for p in P)
    solver.Add(labor_lhs <= 30 * (W_fixed + N_temp))

    # Constraint B: Raw Material
    # sum(b_p * x_p) <= M_avail
    material_lhs = sum(b[p - 1] * x[p] for p in P)
    solver.Add(material_lhs <= M_avail)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()