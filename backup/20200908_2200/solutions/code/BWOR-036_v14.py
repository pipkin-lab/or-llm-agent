from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Parameters
    P = [410, 430, 460, 450]
    S = [425, 440, 465, 455]
    D = [100, 140, 200, 160]
    C_max = 20

    # Decision variables x[i, j] for 1 <= i <= j <= 4
    # Using 0-based indexing: i in 0..3, j in 0..3, i <= j
    x = dict()
    for i in range(4):
        for j in range(i, 4):
            x[i, j] = solver.NumVar(0, inf, 'x_' + str(i) + '_' + str(j))

    # Objective function
    # Maximize Z = sum (S[j] - P[i] - U[i,j]) * x[i,j]
    # U[i,j] = 0 if i == j, else 70 + 100*(j - i)
    obj_terms = []
    for i in range(4):
        for j in range(i, 4):
            if i == j:
                U = 0
            else:
                U = 70 + 100 * (j - i)
            coeff = S[j] - P[i] - U
            obj_terms.append(coeff * x[i, j])

    solver.Maximize(sum(obj_terms))

    # Constraint 1: Sales volume (demand limits)
    # For each quarter j, sum of x[i, j] for i <= j <= D[j]
    for j in range(4):
        demand_expr = sum(x[i, j] for i in range(j + 1))
        solver.Add(demand_expr <= D[j])

    # Constraint 2: Storage capacity
    # End of quarter t (0-based t), inventory = sum of x[i, k] where i <= t < k
    # For t in 0, 1, 2 (end of winter, spring, summer)
    for t in range(3):
        inv_expr = 0
        for i in range(t + 1):
            for k in range(t + 1, 4):
                if i <= t and k > t:
                    inv_expr += x[i, k]
        solver.Add(inv_expr <= C_max)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()