from ortools.linear_solver import pywraplp

def solve_production_planning():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Parameters
    T = 6
    demand = [1, 2, 5, 3, 2, 1]  # in hundreds of units
    C_prod = 10000  # yuan per 100 units
    C_fix = 4000    # yuan
    C_store = 1000  # yuan per 100 units per month
    P_cap = 4       # hundreds of units
    I_cap = 3       # hundreds of units
    
    # Decision Variables
    x = {}
    y = {}
    I = {}
    
    for t in range(T):
        x[t] = solver.NumVar(0, solver.infinity(), 'x_' + str(t))
        y[t] = solver.BoolVar('y_' + str(t))
        I[t] = solver.NumVar(0, I_cap, 'I_' + str(t))
    
    # Objective Function
    objective = 0
    for t in range(T):
        objective += C_prod * x[t] + C_fix * y[t] + C_store * I[t]
    
    solver.Minimize(objective)
    
    # Constraints
    # A. Inventory Balance: I_t = I_{t-1} + x_t - D_t
    # I_0 = 0
    for t in range(T):
        if t == 0:
            # I_0 = 0 + x_0 - D_0 => I_0 - x_0 = -D_0
            solver.Add(I[0] - x[0] == -demand[0])
        else:
            # I_t = I_{t-1} + x_t - D_t => I_t - I_{t-1} - x_t = -D_t
            solver.Add(I[t] - I[t - 1] - x[t] == -demand[t])
    
    # B. Final Inventory Constraint: I_6 = 0 (I_5 in 0-indexed)
    solver.Add(I[T - 1] == 0)
    
    # C. Production Capacity: x_t <= P_cap
    for t in range(T):
        solver.Add(x[t] <= P_cap)
    
    # D. Warehouse Capacity: I_t <= I_cap (already in bounds, but explicit for clarity if needed)
    # Already handled by NumVar bounds, but adding explicitly is safe.
    for t in range(T):
        solver.Add(I[t] <= I_cap)
    
    # E. Big-M Constraint: x_t <= P_cap * y_t
    for t in range(T):
        solver.Add(x[t] <= P_cap * y[t])
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_planning()