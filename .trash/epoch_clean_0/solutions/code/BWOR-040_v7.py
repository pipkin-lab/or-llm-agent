from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver")
        return

    infinity = solver.infinity()

    # Decision Variables
    x1 = solver.NumVar(0, infinity, 'x1')
    x2 = solver.NumVar(0, infinity, 'x2')
    x3 = solver.NumVar(0, infinity, 'x3')
    T = solver.NumVar(0, infinity, 'T')

    # Objective Function
    # Maximize Z = 2*x1 + 3*x2 + 1*x3 - 40*T
    solver.Maximize(2 * x1 + 3 * x2 + 1 * x3 - 40 * T)

    # Constraints
    # A. Labor Capacity Constraint: (x1 + x2 + x3) / 30 <= 100 + T
    # Rearranged: x1/30 + x2/30 + x3/30 - T <= 100
    solver.Add(x1 / 30 + x2 / 30 + x3 / 30 - T <= 100)

    # B. Raw Material (Paper) Constraint: (10/3)*x1 + (40/3)*x2 + (80/3)*x3 <= 30000
    # Simplified: x1 + 4*x2 + 8*x3 <= 9000
    solver.Add(x1 + 4 * x2 + 8 * x3 <= 9000)

    # Solve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    main()