from ortools.linear_solver import pywraplp

def solve_assignment_problem():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Parameters
    I = range(5)  # Companies
    J = range(5)  # Stores
    
    # Cost matrix c[i][j]
    c = [
        [4, 8, 7, 15, 12],
        [7, 9, 17, 14, 10],
        [6, 9, 12, 8, 7],
        [6, 7, 14, 6, 10],
        [6, 9, 12, 10, 6]
    ]
    
    # Decision variables x[i, j]
    x = {}
    for i in I:
        for j in J:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))
    
    # Objective function: minimize total cost
    objective = 0
    for i in I:
        for j in J:
            objective += c[i][j] * x[i, j]
    solver.Minimize(objective)
    
    # Constraints
    # 1. Each store must be built by exactly one company
    for j in J:
        solver.Add(sum(x[i, j] for i in I) == 1)
    
    # 2. Each company is assigned to exactly one store
    for i in I:
        solver.Add(sum(x[i, j] for j in J) == 1)
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_assignment_problem()