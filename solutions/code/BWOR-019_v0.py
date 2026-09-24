from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Index set: players 1 through 8 (1-indexed)
    I = [1, 2, 3, 4, 5, 6, 7, 8]

    # Parameters
    H = dict()
    H[1] = 1.92
    H[2] = 1.90
    H[3] = 1.88
    H[4] = 1.86
    H[5] = 1.85
    H[6] = = 1.83
    H[7] = 1.80
    H[8] = 1.78

    # Decision variables: x_i in {0,1}
    x = dict()
    for i in I:
        x[i] = solver.BoolVar('x_' + str(i))

    # Objective: maximize total height
    obj_terms = []
    for i in I:
        obj_terms.append(H[i] * x[i])
    objective = 0
    for term in obj_terms:
        objective += term
    solver.Maximize(objective)

    # Constraint 1: Exactly 5 players selected
    solver.Add(sum(x[i] for i in I) == 5)

    # Constraint 2: Exactly one center (players 1 and 2)
    solver.Add(x[1] + x[2] == 1)

    # Constraint 3: At least one forward (players 3, 4, 5)
    solver.Add(x[3] + x[4] + x[5] >= 1)

    # Constraint 4: Logical constraints for players 1, 4, 6
    solver.Add(x[1] <= x[6])
    solver.Add(x[4] <= x[6])
    solver.Add(x[1] + x[6] <= 1)
    solver.Add(x[4] + x[6] <= 1)

    # Constraint 5: Mutual exclusion for players 2 and 8
    solver.Add(x[2] + x[8] <= 1)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()