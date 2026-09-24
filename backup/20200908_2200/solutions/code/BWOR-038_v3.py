from ortools.linear_solver import pywraplp

def solve_production_planning():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver")
        return

    infinity = solver.infinity()

    # Decision Variables
    # x_{i, m} : units of product i on machine m
    # X_i : total production of product i

    # Product 1 (I)
    x_1_A1 = solver.NumVar(0, infinity, 'x_1_A1')
    x_1_A2 = solver.NumVar(0, infinity, 'x_1_A2')
    x_1_B1 = solver.NumVar(0, infinity, 'x_1_B1')
    x_1_B2 = solver.NumVar(0, infinity, 'x_1_B2')
    x_1_B3 = solver.NumVar(0, infinity, 'x_1_B3')
    X_1 = solver.NumVar(0, infinity, 'X_1')

    # Product 2 (II)
    x_2_A1 = solver.NumVar(0, infinity, 'x_2_A1')
    x_2_A2 = solver.NumVar(0, infinity, 'x_2_A2')
    x_2_B1 = solver.NumVar(0, infinity, 'x_2_B1') # Based on table data
    X_2 = solver.NumVar(0, infinity, 'X_2')

    # Product 3 (III)
    x_3_A2 = solver.NumVar(0, infinity, 'x_3_A2')
    x_3_B2 = solver.NumVar(0, infinity, 'x_3_B2')
    X_3 = solver.NumVar(0, infinity, 'X_3')

    # Objective Function
    # Max Z = 1.00 X_1 + 1.65 X_2 + 2.30 X_3 
    #         - (0.25 x_1_A1 + 0.21 x_1_A2 + 0.50 x_2_A1 + 0.27 x_2_A2 + 0.36 x_3_A2 
    #            + 0.36 x_1_B1 + 0.44 x_1_B2 + 0.35 x_1_B3 + 0.48 x_2_B1 + 1.21 x_3_B2)

    objective = solver.Maximize(
        1.00 * X_1 + 1.65 * X_2 + 2.30 * X_3
        - (0.25 * x_1_A1 + 0.21 * x_1_A2 + 0.50 * x_2_A1 + 0.27 * x_2_A2 + 0.36 * x_3_A2
           + 0.36 * x_1_B1 + 0.44 * x_1_B2 + 0.35 * x_1_B3 + 0.48 * x_2_B1 + 1.21 * x_3_B2)
    )

    # Constraints

    # Flow Balance Constraints
    # Product 1
    solver.Add(X_1 - x_1_A1 - x_1_A2 == 0)
    solver.Add(X_1 - x_1_B1 - x_1_B2 - x_1_B3 == 0)
    
    # Product 2
    solver.Add(X_2 - x_2_A1 - x_2_A2 == 0)
    solver.Add(X_2 - x_2_B1 == 0)
    
    # Product 3
    solver.Add(X_3 - x_3_A2 == 0)
    solver.Add(X_3 - x_3_B2 == 0)

    # Machine Capacity Constraints
    # Machine A1: 5 x_1_A1 + 10 x_2_A1 <= 6000
    solver.Add(5 * x_1_A1 + 10 * x_2_A1 <= 6000)
    
    # Machine A2: 7 x_1_A2 + 9 x_2_A2 + 12 x_3_A2 <= 10000
    solver.Add(7 * x_1_A2 + 9 * x_2_A2 + 12 * x_3_A2 <= 10000)
    
    # Machine B1: 6 x_1_B1 + 8 x_2_B1 <= 4000
    solver.Add(6 * x_1_B1 + 8 * x_2_B1 <= 4000)
    
    # Machine B2: 4 x_1_B2 + 11 x_3_B2 <= 7000
    solver.Add(4 * x_1_B2 + 11 * x_3_B2 <= 7000)
    
    # Machine B3: 7 x_1_B3 <= 4000
    solver.Add(7 * x_1_B3 <= 4000)

    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve_production_planning()