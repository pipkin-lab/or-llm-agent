from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()

    # Parameters
    P = {1: 410, 2: 430, 3: 460, 4: 450}
    S = {1: 425, 2: 440, 3: 465, 4: 455}
    D = {1: 100, 2: 140, 3: 200, 4: 160}
    C = 20
    a = 70
    b = 100

    # Decision variables z[i][j] for 1 <= i <= j <= 4
    z = dict()
    for i in range(1, 5):
        for j in range(i, 5):
            z[i, j] = solver.NumVar(0, inf, 'z_' + str(i) + '_' + str(j))

    # Objective function: Maximize total profit
    # Profit coefficient for z[i][j]:
    #   if i == j: S[i] - P[i]
    #   if i < j: S[j] - P[i] - (a + b * (j - i))
    objective = 0
    for i in range(1, 5):
        for j in range(i, 5):
            if i == j:
                coeff = S[i] - P[i]
            else:
                u = j - i
                coeff = S[j] - P[i] - (a + b * u)
            objective += coeff * z[i, j]

    solver.Maximize(objective)

    # Constraints: Sales volume limits
    # For each quarter j, sum_{i=1}^{j} z[i][j] <= D[j]
    for j in range(1, 5):
        sales_expr = 0
        for i in range(1, j + 1):
            sales_expr += z[i, j]
        solver.Add(sales_expr <= D[j])

    # Constraints: Warehouse capacity
    # For each quarter t (1, 2, 3), sum_{i=1}^{t} sum_{j=t+1}^{4} z[i][j] <= C
    for t in range(1, 4):
        inv_expr = 0
        for i in range(1, t + 1):
            for j in range(t + 1, 5):
                inv_expr += z[i, j]
        solver.Add(inv_expr <= C)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()