from ortools.linear_solver import pywraplp

def solve_course_selection():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print("Could not create solver")
        return

    # Courses
    courses = ['Calc', 'OR', 'DataStruct', 'MgmtStats', 'CompSim', 'CompProg', 'Forecast']
    
    # Create binary decision variables
    x = dict()
    for c in courses:
        x[c] = solver.BoolVar('x_' + c)

    # Objective: Minimize total number of courses
    objective = sum(x[c] for c in courses)
    solver.Minimize(objective)

    # Category requirements
    # Math: Calc + OR + DataStruct + MgmtStats + Forecast >= 2
    solver.Add(x['Calc'] + x['OR'] + x['DataStruct'] + x['MgmtStats'] + x['Forecast'] >= 2)
    
    # OR: OR + MgmtStats + CompSim + Forecast >= 2
    solver.Add(x['OR'] + x['MgmtStats'] + x['CompSim'] + x['Forecast'] >= 2)
    
    # CS: DataStruct + CompSim + CompProg >= 2
    solver.Add(x['DataStruct'] + x['CompSim'] + x['CompProg'] >= 2)

    # Prerequisite constraints
    # CompSim <= CompProg
    solver.Add(x['CompSim'] <= x['CompProg'])
    # DataStruct <= CompProg
    solver.Add(x['DataStruct'] <= x['CompProg'])
    # MgmtStats <= Calc
    solver.Add(x['MgmtStats'] <= x['Calc'])
    # Forecast <= MgmtStats
    solver.Add(x['Forecast'] <= x['MgmtStats'])

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_course_selection()