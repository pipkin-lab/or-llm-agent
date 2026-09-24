from ortools.linear_solver import pywraplp

def solve_toy_distribution():
    # Create the solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("Could not create solver")
        return

    # Define the sets
    toys = ['A', 'B', 'C']
    stores = ['X', 'Y', 'Z']

    # Define parameters
    supply = {
        'A': 1000,
        'B': 2000,
        'C': 2000
    }

    # Profit margins p[i][j]
    # Note: p[A][Z] is 0 and x[A][Z] is fixed to 0
    profit = {
        'A': {'X': 5, 'Y': 4, 'Z': 0},
        'B': {'X': 16, 'Y': 8, 'Z': 6},
        'C': {'X': 12, 'Y': 10, 'Z': 11}
    }

    # Per-link capacity (demand per toy per store)
    link_capacity = 1500

    # Create decision variables
    # x[i][j] is the number of units of toy i shipped to store j
    x = {}
    for i in toys:
        for j in stores:
            # If i='A' and j='Z', the constraint says x[A][Z] = 0.
            # We can either create the variable and add constraint x=0, or skip it.
            # The prompt says "x[A,Z] = 0 (Constraint)" and "x[A,Z] is excluded... or setting its coefficient to 0/upper bound to 0".
            # Let's create the variable for all pairs to keep the structure uniform, but enforce bounds.
            if i == 'A' and j == 'Z':
                x[i, j] = solver.NumVar(0, 0, f'x_{i}_{j}')
            else:
                # Upper bound is min(supply[i], link_capacity) effectively, but supply is a sum constraint.
                # The individual link capacity is 1500.
                x[i, j] = solver.NumVar(0, solver.infinity(), f'x_{i}_{j}')
                # Add the individual link capacity constraint: x[i][j] <= 1500
                solver.Add(x[i, j] <= link_capacity)

    # Objective Function: Maximize total profit
    objective = solver.Objective()
    for i in toys:
        for j in stores:
            objective.SetCoefficient(x[i, j], profit[i][j])
    solver.Maximize(objective)

    # Constraints

    # 1. Supply Constraints: Total outflow for each toy <= supply limit
    for i in toys:
        total_outflow = sum(x[i, j] for j in stores)
        solver.Add(total_outflow <= supply[i])

    # 3. Specific Operational Constraints
    # Store Z requires at least 1,000 units of Toy C
    solver.Add(x['C', 'Z'] >= 1000)

    # Solve the problem
    status = solver.Solve()

    # Check if the solution is optimal
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
        
        # Print the solution details for verification
        total_profit = 0
        for i in toys:
            for j in stores:
                val = x[i, j].solution_value()
                if val > 0:
                    print(f"Ship {val} units of Toy {i} to Store {j}")
                    total_profit += val * profit[i][j]
        
        # Verify supply constraints
        for i in toys:
            total_shipped = sum(x[i, j].solution_value() for j in stores)
            print(f"Total Toy {i} shipped: {total_shipped} (Supply: {supply[i]})")
            
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve_toy_distribution()