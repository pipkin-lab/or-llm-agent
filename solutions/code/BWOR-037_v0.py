from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()

    # Decision variables
    x_1A = solver.IntVar(0, INF, 'x_1A')
    x_1B = solver.IntVar(0, INF, 'x_1B')
    x_2A = solver.IntVar(0, INF, 'x_2A')
    x_2B = solver.IntVar(0, INF, 'x_2B')
    x_3A = solver.IntVar(0, INF, 'x_3A')
    x_3B = solver.IntVar(0, INF, 'x_3B')

    # Objective: Minimize total weekly wage cost
    # Coefficients: x_1A=100, x_1B=260, x_2A=100, x_2B=80, x_3A=400, x_3B=340
    objective = solver.Objective()
    objective.SetCoefficient(x_1A, 100)
    objective.SetCoefficient(x_1B, 260)
    objective.SetCoefficient(x_2A, 100)
    objective.SetCoefficient(x_2B, 80)
    objective.SetCoefficient(x_3A, 400)
    objective.SetCoefficient(x_3B, 340)
    objective.SetMinimization()

    # Task 1: 42*x_1A + 114*x_1B >= 10000
    c1 = solver.Constraint(10000, INF, 'task1_hours')
    c1.SetCoefficient(x_1A, 42)
    c1.SetCoefficient(x_1B, 114)

    # Task 2: 42*x_2A + 36*x_2B >= 20000
    c2 = solver.Constraint(20000, INF, 'task2_hours')
    c2.SetCoefficient(x_2A, 42)
    c2.SetCoefficient(x_2B, 36)

    # Task 3: 180*x_3A + 150*x_3B >= 30000
    c3 = solver.Constraint(30000, INF, 'task3_hours')
    c3.SetCoefficient(x_3A, 180)
    c3.SetCoefficient(x_3B, 150)

    # Technician capacity: x_1A + x_1B + x_2A + x_3B <= 400
    c4 = solver.Constraint(0, 400, 'tech_capacity')
    c4.SetCoefficient(x_1A, 1)
    c4.SetCoefficient(x_1B, 1)
    c4.SetCoefficient(x_2A, 1)
    c4.SetCoefficient(x_3B, 1)

    # Laborer capacity: 2*x_1B + x_2B + 5*x_3A + 3*x_3B <= 800
    c5 = solver.Constraint(0, 800, 'laborer_capacity')
    c5.SetCoefficient(x_1B, 2)
    c5.SetCoefficient(x_2B, 1)
    c5.SetCoefficient(x_3A, 5)
    c5.SetCoefficient(x_3B, 3)

    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()