from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("NO_FEASIBLE_SOLUTION")
        return

    # Indices
    # 1=Ca, 2=OR, 3=DS, 4=MS, 5=CSim, 6=CP, 7=F
    n_courses = 7

    # Decision Variables
    x = {}
    for i in range(1, n_courses + 1):
        x[i] = solver.IntVar(0, 1, 'x_' + str(i))

    # Objective: Minimize total number of courses
    objective = 0
    for i in range(1, n_courses + 1):
        objective += x[i]
    solver.Minimize(objective)

    # Constraints
    # A. Category Requirements
    # Math: x1 + x2 + x3 + x4 + x7 >= 2
    solver.Add(x[1] + x[2] + x[3] + x[4] + x[7] >= 2)
    
    # OR: x2 + x4 + x5 + x7 >= 2
    solver.Add(x[2] + x[4] + x[5] + x[7] >= 2)
    
    # CS: x3 + x5 + x6 >= 2
    solver.Add(x[3] + x[5] + x[6] >= 2)

    # B. Prerequisite Constraints
    # 1. CSim (5) requires CP (6): x6 >= x5
    solver.Add(x[6] >= x[5])
    
    # 2. DS (3) requires CP (6): x6 >= x3
    solver.Add(x[6] >= x[3])
    
    # 3. MS (4) requires Ca (1): x1 >= x4
    solver.Add(x[1] >= x[4])
    
    # 4. F (7) requires MS (4): x4 >= x7
    solver.Add(x[4] >= x[7])

    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()