from ortools.linear_solver import pywraplp

def solve_course_selection():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    inf = solver.infinity()

    # Course indices
    # 0: Calculus (Ca)
    # 1: Operations Research (OR)
    # 2: Data Structures (DS)
    # 3: Managerial Statistics (MS)
    # 4: Computer Simulation (CS)
    # 5: Computer Programming (CP)
    # 6: Forecasting (F)

    n_courses = 7
    x = dict()
    for i in range(n_courses):
        x[i] = solver.BoolVar('x_' + str(i))

    # Objective: Minimize total courses
    objective_terms = []
    for i in range(n_courses):
        objective_terms.append(x[i])
    solver.Minimize(sum(objective_terms))

    # Category Requirements
    # Math: Ca(0), OR(1), DS(2), MS(3), F(6) >= 2
    math_courses = [0, 1, 2, 3, 6]
    solver.Add(sum(x[i] for i in math_courses) >= 2)

    # OR: OR(1), MS(3), CS(4), F(6) >= 2
    or_courses = [1, 3, 4, 6]
    solver.Add(sum(x[i] for i in or_courses) >= 2)

    # CS: DS(2), CS(4), CP(5) >= 2
    cs_courses = [2, 4, 5]
    solver.Add(sum(x[i] for i in cs_courses) >= 2)

    # Prerequisite Constraints
    # CS(4) requires CP(5): x[4] <= x[5]
    solver.Add(x[4] <= x[5])

    # DS(2) requires CP(5): x[2] <= x[5]
    solver.Add(x[2] <= x[5])

    # MS(3) requires Ca(0): x[3] <= x[0]
    solver.Add(x[3] <= x[0])

    # F(6) requires MS(3): x[6] <= x[3]
    solver.Add(x[6] <= x[3])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_course_selection()