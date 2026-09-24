from ortools.linear_solver import pywraplp

def solve_production_planning():
    T = [1, 2, 3, 4]
    
    C = dict()
    C[1] = 25
    C[2] = 35
    C[3] = 30
    C[4] = 20
    
    D = dict()
    D[1] = 15
    D[2] = 20
    D[3] = 25
    D[4] = 20
    
    p = dict()
    p[1] = 12.0
    p[2] = 11.0
    p[3] = 11.5
    p[4] = 12.5
    
    h = 0.1
    
    solver = pywraplp.Solver.CreateSolver('GLOP')
    inf = solver.infinity()
    
    x = dict()
    I = dict()
    
    for t in T:
        x[t] = solver.NumVar(0, inf, 'x_' + str(t))
        I[t] = solver.NumVar(0, inf, 'I_' + str(t))
    
    for t in T:
        solver.Add(x[t] <= C[t])
    
    for t in T:
        if t == 1:
            solver.Add(x[1] - I[1] == D[1])
        else:
            prev = t - 1
            solver.Add(I[prev] + x[t] - I[t] == D[t])
    
    solver.Add(I[4] == 0)
    
    obj_terms = []
    for t in T:
        obj_terms.append(p[t] * x[t])
    for t in T:
        obj_terms.append(h * I[t])
    
    obj = sum(obj_terms)
    solver.Minimize(obj)
    
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve_production_planning()