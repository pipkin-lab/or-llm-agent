from ortools.linear_solver import pywraplp

def solve():
    # Define the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Parameters
    # Routes: 0: E->D, 1: B->C, 2: A->F, 3: D->B
    n_routes = 4
    
    # Sailing times (symmetric in this problem)
    # We need T[O, D] for each route
    # Route 0: E->D, T=17
    # Route 1: B->C, T=3
    # Route 2: A->F, T=7
    # Route 3: D->B, T=13
    
    # Frequencies (sailings per day)
    # Route 0: 3
    # Route 1: 2
    # Route 2: 1
    # Route 3: 1
    
    # Port time (1 day unload + 1 day load = 2 days per cycle)
    t_port = 2
    
    # Data for each route: (T_out, T_back, frequency)
    # Since the matrix is symmetric, T_out == T_back
    route_data = [
        (17, 17, 3),  # Route 1: E->D
        (3, 3, 2),     # Route 2: B->C
        (7, 7, 1),     # Route 3: A->F
        (13, 13, 1)    # Route 4: D->B
    ]
    
    # Decision Variables
    # N[r] = Number of ships for route r
    # Bounds: 0 to infinity (integer)
    N = dict()
    for r in range(n_routes):
        N[r] = solver.IntVar(0, solver.infinity(), 'N_' + str(r))
    
    # Objective: Minimize total ships
    objective = 0
    for r in range(n_routes):
        objective += N[r]
    
    solver.Minimize(objective)
    
    # Constraints
    # For each route r:
    # Cycle time C_r = T_out + T_back + 2 * t_port
    # Required ships N_r >= f_r * C_r
    for r in range(n_routes):
        T_out, T_back, f = route_data[r]
        C_r = T_out + T_back + 2 * t_port
        min_ships = f * C_r
        
        # N[r] >= min_ships
        solver.Add(N[r] >= min_ships)
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

if __name__ == '__main__':
    solve()