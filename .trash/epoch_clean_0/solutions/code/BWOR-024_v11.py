from ortools.linear_solver import pywraplp

def main():
    # Index sets
    J = [1, 2, 3, 4, 5, 6]
    K = [1, 2, 3, 4, 5, 6]

    # Parameters
    A = dict()
    B = dict()
    A[1] = 30
    A[2] = 60
    A[3] = 60
    A[4] = 20
    A[5] = 80
    A[6] = 90

    B[1] = 70
    B[2] = 70
    B[3] = 50
    B[4] = 60
    B[5] = 30
    B[6] = 40

    # Solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Decision variables
    x = dict()
    for j in J:
        for k in K:
            x[j, k] = solver.BoolVar('x_' + str(j) + '_' + str(k))

    T_A = dict()
    T_B = dict()
    for k in K:
        T_A[k] = solver.NumVar(0, inf, 'T_A_' + str(k))
        T_B[k] = solver.NumVar(0, inf, 'T_B_' + str(k))

    C_max = solver.NumVar(0, inf, 'C_max')

    # Assignment constraints: each job to exactly one position
    for j in J:
        solver.Add(sum(x[j, k] for k in K) == 1)

    # Assignment constraints: each position to exactly one job
    for k in K:
        solver.Add(sum(x[j, k] for j in J) == 1)

    # Machine A timing constraints
    # T_A[1] = sum_j A_j * x[j,1]
    solver.Add(T_A[1] == sum(A[j] * x[j, 1] for j in J))

    for k in K[1:]:
        solver.Add(T_A[k] == sum(A[j] * x[j, k] for j in J) + T_A[k - 1])

    # Machine B timing constraints
    # T_B[1] = T_A[1] + sum_j B_j * x[j,1]
    solver.Add(T_B[1] == T_A[1] + sum(B[j] * x[j, 1] for j in J))

    for k in K[1:]:
        # T_B[k] >= T_B[k-1] + sum_j B_j * x[j,k]
        solver.Add(T_B[k] >= T_B[k - 1] + sum(B[j] * x[j, k] for j in J))
        # T_B[k] >= T_A[k] + sum_j B_j * x[j,k]
        solver.Add(T_B[k] >= T_A[k] + sum(B[j] * x[j, k] for j in J))

    # Makespan definition
    for k in K:
        solver.Add(C_max >= T_B[k])

    # Objective: minimize C_max
    solver.Minimize(C_max)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()