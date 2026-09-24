from ortools.linear_solver import pywraplp

def solve_production_planning():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("NO_FEASIBLE_SOLUTION")
        return

    infinity = solver.infinity()

    # Decision Variables
    # Stage A variables
    xA_A1_1 = solver.NumVar(0, infinity, 'xA_A1_1')
    xA_A2_1 = solver.NumVar(0, infinity, 'xA_A2_1')
    xA_A1_2 = solver.NumVar(0, infinity, 'xA_A1_2')
    xA_A2_2 = solver.NumVar(0, infinity, 'xA_A2_2')
    xA_A2_3 = solver.NumVar(0, infinity, 'xA_A2_3')

    # Stage B variables
    xB_B1_1 = solver.NumVar(0, infinity, 'xB_B1_1')
    xB_B2_1 = solver.NumVar(0, infinity, 'xB_B2_1')
    xB_B3_1 = solver.NumVar(0, infinity, 'xB_B3_1')
    xB_B1_2 = solver.NumVar(0, infinity, 'xB_B1_2')
    xB_B2_3 = solver.NumVar(0, infinity, 'xB_B2_3')

    # Objective Function
    # Max Z = 0.75*xA_A1_1 + 0.79*xA_A2_1 - 0.36*xB_B1_1 - 0.44*xB_B2_1 - 0.35*xB_B3_1
    #       + 1.15*xA_A1_2 + 1.38*xA_A2_2 - 0.48*xB_B1_2
    #       + 1.94*xA_A2_3 - 1.21*xB_B2_3
    
    objective = solver.Objective()
    objective.SetCoefficient(xA_A1_1, 0.75)
    objective.SetCoefficient(xA_A2_1, 0.79)
    objective.SetCoefficient(xB_B1_1, -0.36)
    objective.SetCoefficient(xB_B2_1, -0.44)
    objective.SetCoefficient(xB_B3_1, -0.35)
    objective.SetCoefficient(xA_A1_2, 1.15)
    objective.SetCoefficient(xA_A2_2, 1.38)
    objective.SetCoefficient(xB_B1_2, -0.48)
    objective.SetCoefficient(xA_A2_3, 1.94)
    objective.SetCoefficient(xB_B2_3, -1.21)
    objective.SetMaximization()

    # Constraints
    
    # 1. Flow Balance Constraints
    # Product I: xA_A1_1 + xA_A2_1 = xB_B1_1 + xB_B2_1 + xB_B3_1
    solver.Add(xA_A1_1 + xA_A2_1 == xB_B1_1 + xB_B2_1 + xB_B3_1, 'Flow_Bal_I')
    
    # Product II: xA_A1_2 + xA_A2_2 = xB_B1_2
    solver.Add(xA_A1_2 + xA_A2_2 == xB_B1_2, 'Flow_Bal_II')
    
    # Product III: xA_A2_3 = xB_B2_3
    solver.Add(xA_A2_3 == xB_B2_3, 'Flow_Bal_III')

    # 2. Machine Capacity Constraints
    # Machine A1: 5*xA_A1_1 + 10*xA_A1_2 <= 6000
    solver.Add(5 * xA_A1_1 + 10 * xA_A1_2 <= 6000, 'Cap_A1')
    
    # Machine A2: 7*xA_A2_1 + 9*xA_A2_2 + 12*xA_A2_3 <= 10000
    solver.Add(7 * xA_A2_1 + 9 * xA_A2_2 + 12 * xA_A2_3 <= 10000, 'Cap_A2')
    
    # Machine B1: 6*xB_B1_1 + 8*xB_B1_2 <= 4000
    solver.Add(6 * xB_B1_1 + 8 * xB_B1_2 <= 4000, 'Cap_B1')
    
    # Machine B2: 4*xB_B2_1 + 11*xB_B2_3 <= 7000
    solver.Add(4 * xB_B2_1 + 11 * xB_B2_3 <= 7000, 'Cap_B2')
    
    # Machine B3: 7*xB_B3_1 <= 4000
    solver.Add(7 * xB_B3_1 <= 4000, 'Cap_B3')

    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve_production_planning()