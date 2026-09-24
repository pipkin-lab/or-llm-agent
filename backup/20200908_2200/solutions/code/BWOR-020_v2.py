from ortools.linear_solver import pywraplp

def solve_truck_delivery_problem():
    # Define the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if solver is None:
        print("Could not create SCIP solver")
        return

    # Define sets
    I = ['A', 'B', 'C', 'D', 'E']  # Customers
    J = [1, 2, 3, 4]               # Trucks

    # Define parameters
    d = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 8}  # Demand
    K = {1: 2, 2: 6, 3: 8, 4: 11}                 # Capacity
    # Cost of using truck j (not explicitly given, so we assume placeholder values)
    # The problem statement lists c_j but doesn't provide values.
    # For a complete executable script, we need to define them.
    # Let's assign some representative costs.
    c = {1: 5, 2: 8, 3: 10, 4: 15}

    # Define decision variables
    # x[i][j] = 1 if customer i is assigned to truck j
    x = {}
    for i in I:
        for j in J:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))

    # y[j] = 1 if truck j is used
    y = {}
    for j in J:
        y[j] = solver.BoolVar('y_{}'.format(j))

    # Objective function: Minimize total cost
    objective = 0
    for j in J:
        objective += c[j] * y[j]
    solver.Minimize(objective)

    # Constraint 1: Each customer must be assigned to exactly one truck
    for i in I:
        solver.Add(sum(x[i, j] for j in J) == 1)

    # Constraint 2: Truck capacity constraints
    for j in J:
        solver.Add(sum(d[i] * x[i, j] for i in I) <= K[j] * y[j])

    # Constraint 3: Mutual exclusion constraints
    # A truck cannot deliver to both Customer A and Customer C
    for j in J:
        solver.Add(x['A', j] + x['C', j] <= 1)

    # A truck cannot deliver to both Customer B and Customer D
    for j in J:
        solver.Add(x['B', j] + x['D', j] <= 1)

    # Solve the model
    status = solver.Solve()

    # Check the status of the solution
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == "__main__":
    solve_truck_delivery_problem()