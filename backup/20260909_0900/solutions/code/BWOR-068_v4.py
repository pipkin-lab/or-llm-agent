from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    infinity = solver.infinity()
    
    # Parameters
    T = [1, 2, 3, 4, 5, 6]
    K = [1, 2, 3, 4, 5]
    
    D = {1: 40, 2: 20, 3: 30, 4: 40, 5: 30, 6: 20}
    Q = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
    C_var = {1: 48, 2: 86, 3: 118, 4: 138, 5: 160}
    C_fixed = 10
    h = 0.2
    I_max = 40
    
    # Decision Variables
    x = dict()
    for t in T:
        for k in K:
            x[t, k] = solver.BoolVar('x_' + str(t) + '_' + str(k))
            
    I = dict()
    for t in T:
        I[t] = solver.NumVar(0, I_max, 'I_' + str(t))
        
    # Objective Function
    objective = 0
    for t in T:
        for k in K:
            objective += (C_var[k] + C_fixed) * x[t, k]
        objective += h * I[t]
        
    solver.Minimize(objective)
    
    # Constraints
    
    # 1. Order Selection Constraint: At most one order level per month
    for t in T:
        solver.Add(sum(x[t, k] for k in K) <= 1)
        
    # 2. Inventory Balance Constraint
    # I_t = I_{t-1} + Order_t - D_t
    # I_0 = 0
    # I_6 = 0
    
    for t in T:
        order_t = sum(Q[k] * x[t, k] for k in K)
        
        if t == 1:
            # I_1 = I_0 + Order_1 - D_1, where I_0 = 0
            solver.Add(I[t] == order_t - D[t])
        else:
            # I_t = I_{t-1} + Order_t - D_t
            solver.Add(I[t] == I[t-1] + order_t - D[t])
            
    # Boundary Condition: End of season inventory I_6 = 0
    solver.Add(I[6] == 0)
    
    # 3. Inventory Capacity Constraint is handled by variable bounds (0 to I_max)
    # 4. Non-negativity is handled by variable bounds (0 to I_max)
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()