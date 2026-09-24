from ortools.linear_solver import pywraplp

def solve_production_planning():
    # Parameters
    months = range(1, 7)  # T = {1, 2, 3, 4, 5, 6}
    
    D = {1: 3000, 2: 3600, 3: 4000, 4: 4600, 5: 4800, 6: 5000}
    I_0 = 400
    I_max_6 = 100
    h = 10  # holding cost per unit per month
    
    W_0 = 80  # initial skilled workers
    H_cap = 160  # max hours per skilled worker per month
    h_train = 50  # hours per trainee per month
    r = 0.02  # attrition rate
    a_train = 800  # trainee allowance
    w_skilled = 2000  # skilled worker salary
    time_per_unit = 4  # hours per unit
    cost_material = 150  # material cost per unit
    price = 240  # selling price per unit
    
    # Solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if solver is None:
        print("Could not create solver")
        return
    
    # Variables
    # Continuous variables: W[t], N[t], P[t], I[t] for t in 1..6
    W = dict()
    N = dict()
    P = dict()
    I = dict()
    
    for t in months:
        W[t] = solver.NumVar(0, solver.infinity(), 'W_' + str(t))
        N[t] = solver.NumVar(0, solver.infinity(), 'N_' + str(t))
        P[t] = solver.NumVar(0, solver.infinity(), 'P_' + str(t))
        I[t] = solver.NumVar(0, solver.infinity(), 'I_' + str(t))
    
    # Constraints
    
    # 1. Workforce Initialization: W_1 = 80
    solver.Add(W[1] == W_0)
    
    # 2. Workforce Transition: W[t] = 0.98 * W[t-1] + N[t-1] for t = 2..6
    for t in range(2, 7):
        solver.Add(W[t] == (1 - r) * W[t - 1] + N[t - 1])
    
    # 3. Labor Capacity: 4 * P[t] + 50 * N[t] <= 160 * W[t] for all t
    for t in months:
        solver.Add(time_per_unit * P[t] + h_train * N[t] <= H_cap * W[t])
    
    # 4. Inventory Balance
    # I[1] = I_0 + P[1] - D[1]
    solver.Add(I[1] == I_0 + P[1] - D[1])
    
    # I[t] = I[t-1] + P[t] - D[t] for t = 2..6
    for t in range(2, 7):
        solver.Add(I[t] == I[t - 1] + P[t] - D[t])
    
    # 5. Inventory Limits
    # I[6] <= 100
    solver.Add(I[6] <= I_max_6)
    
    # Objective: Maximize sum over t of (90 * P[t] - 2000 * W[t] - 800 * N[t] - 10 * I[t])
    # This is equivalent to: 240*P - 150*P - 2000*W - 800*N - 10*I
    objective_terms = []
    for t in months:
        objective_terms.append((price - cost_material) * P[t])
        objective_terms.append(-w_skilled * W[t])
        objective_terms.append(-a_train * N[t])
        objective_terms.append(-h * I[t])
    
    solver.Maximize(sum(objective_terms))
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_planning()