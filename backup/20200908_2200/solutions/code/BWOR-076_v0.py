from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()

    T = [1, 2, 3, 4]
    A = [0, 1, 2, 3, 4]

    # Parameters
    C_buy = {1: 2.5, 2: 2.6, 3: 2.8, 4: 3.1}
    S = {1: 2.0, 2: 1.6, 3: 1.3, 4: 1.1}
    M = {1: 0.3, 2: 0.8, 3: 1.5, 4: 2.0}

    # Decision Variables
    # x[i, j] = 1 if machine bought at start of year i and sold at end of year j
    x = {}
    for i in T:
        for j in range(i, 5):  # j from i to 4
            x[i, j] = solver.BoolVar(f'x_{i}_{j}')

    # Objective Function
    # Minimize total cost
    objective = 0
    for i in T:
        for j in range(i, 5):
            # Calculate cost for buying at i and selling at j
            # Purchase cost
            cost = C_buy[i]
            # Operating costs: machine used in years i, i+1, ..., j
            # Age in year k (where k from i to j) is k - i + 1
            for k in range(i, j + 1):
                age = k - i + 1
                cost += M[age]
            # Salvage value credit
            total_age = j - i + 1
            cost -= S[total_age]
            
            objective += cost * x[i, j]

    solver.Minimize(objective)

    # Constraints

    # 1. Start Constraint: A machine must be purchased at the beginning of Year 1.
    # sum_{j=1}^{4} x[1, j] = 1
    solver.Add(sum(x[1, j] for j in range(1, 5)) == 1)

    # 2. Continuity/Linkage Constraints
    # For t = 1: sum_{i=1}^{1} x[i, 1] = sum_{j=2}^{4} x[2, j]
    solver.Add(sum(x[i, 1] for i in range(1, 2)) == sum(x[2, j] for j in range(2, 5)))

    # For t = 2: sum_{i=1}^{2} x[i, 2] = sum_{j=3}^{4} x[3, j]
    solver.Add(sum(x[i, 2] for i in range(1, 3)) == sum(x[3, j] for j in range(3, 5)))

    # For t = 3: sum_{i=1}^{3} x[i, 3] = sum_{j=4}^{4} x[4, j]
    solver.Add(sum(x[i, 3] for i in range(1, 4)) == sum(x[4, j] for j in range(4, 5)))

    # 3. End Constraint: A machine must be sold at the end of the planning horizon (Year 4).
    # sum_{i=1}^{4} x[i, 4] = 1
    solver.Add(sum(x[i, 4] for i in range(1, 5)) == 1)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve()