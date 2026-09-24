from ortools.linear_solver import pywraplp

def solve():
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Parameters
    w = [2, 3, 4]
    p = [100, 140, 180]
    W_max = 10
    I = [0, 1, 2]  # product types 1, 2, 3 (0-indexed)
    
    # Decision variables: x_i for each product type i
    x = dict()
    for i in I:
        x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i + 1))
    
    # Objective: Maximize total profit
    obj_terms = []
    for i in I:
        obj_terms.append(p[i] * x[i])
    solver.Maximize(sum(obj_terms))
    
    # Constraint: Total weight <= W_max
    weight_terms = []
    for i in I:
        weight_terms.append(w[i] * x[i])
    solver.Add(sum(weight_terms) <= W_max)
    
    # Solve
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("OPTIMAL_VALUE:", solver.Objective().Value())
    else:
        print("NO_FEASIBLE_SOLUTION")

solve()