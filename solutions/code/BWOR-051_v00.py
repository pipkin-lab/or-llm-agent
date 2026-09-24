from ortools.linear_solver import pywraplp

def solve_scenario_a():
    persons = ['X', 'Y', 'Z', 'R']
    tasks = ['A', 'B', 'C', 'D', 'F']
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    
    # Decision variables x[i][j]
    x = dict()
    for i in persons:
        for j in tasks:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))
    
    # Cost coefficients
    cost = dict()
    cost[('X', 'A')] = 25
    cost[('X', 'B')] = 29
    cost[('X', 'C')] = 31
    cost[('X', 'D')] = 42
    cost[('X', 'F')] = 37
    cost[('Y', 'A')] = 39
    cost[('Y', 'B')] = 38
    cost[('Y', 'C')] = 26
    cost[('Y', 'D')] = 20
    cost[('Y', 'F')] = 33
    cost[('Z', 'A')] = 34
    cost[('Z', 'B')] = 27
    cost[('Z', 'C')] = 28
    cost[('Z', 'D')] = 40
    cost[('Z', 'F')] = 32
    cost[('R', 'A')] = 24
    cost[('R', 'B')] = 42
    cost[('R', 'C')] = 36
    cost[('R', 'D')] = 23
    cost[('R', 'F')] = 45
    
    # Objective: Minimize total cost
    obj_terms = []
    for i in persons:
        for j in tasks:
            obj_terms.append(cost[(i, j)] * x[i, j])
    solver.Minimize(sum(obj_terms))
    
    # Each task assigned exactly once
    for j in tasks:
        solver.Add(sum(x[i, j] for i in persons) == 1)
    
    # Each person gets 1 or 2 tasks
    for i in persons:
        L_i = sum(x[i, j] for j in tasks)
        solver.Add(L_i >= 1)
        solver.Add(L_i <= 2)
    
    # Total assignments = 5 (implied by tasks == 1, but explicit for clarity)
    solver.Add(sum(x[i, j] for i in persons for j in tasks) == 5)
    
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        return solver.Objective().Value()
    else:
        return None

def solve_scenario_b():
    persons = ['X', 'Y', 'Z', 'R']
    tasks = ['A', 'B', 'C', 'D', 'F']
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    
    # Decision variables x[i][j]
    x = dict()
    for i in persons:
        for j in tasks:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))
    
    # Cost coefficients
    cost = dict()
    cost[('X', 'A')] = 25
    cost[('X', 'B')] = 29
    cost[('X', 'C')] = 31
    cost[('X', 'D')] = 42
    cost[('X', 'F')] = 37
    cost[('Y', 'A')] = 39
    cost[('Y', 'B')] = 38
    cost[('Y', 'C')] = 26
    cost[('Y', 'D')] = 20
    cost[('Y', 'F')] = 33
    cost[('Z', 'A')] = 34
    cost[('Z', 'B')] = 27
    cost[('Z', 'C')] = 28
    cost[('Z', 'D')] = 40
    cost[('Z', 'F')] = 32
    cost[('R', 'A')] = 24
    cost[('R', 'B')] = 42
    cost[('R', 'C')] = 36
    cost[('R', 'D')] = 23
    cost[('R', 'F')] = 45
    
    # Objective: Minimize total cost
    obj_terms = []
    for i in persons:
        for j in tasks:
            obj_terms.append(cost[(i, j)] * x[i, j])
    solver.Minimize(sum(obj_terms))
    
    # Each task assigned exactly once
    for j in tasks:
        solver.Add(sum(x[i, j] for i in persons) == 1)
    
    # Y: exactly 1 task
    solver.Add(sum(x['Y', j] for j in tasks) == 1)
    
    # R: exactly 1 task
    solver.Add(sum(x['R', j] for j in tasks) == 1)
    
    # X: 1 or 2 tasks
    LX = sum(x['X', j] for j in tasks)
    solver.Add(LX >= 1)
    solver.Add(LX <= 2)
    
    # Z: 1 or 2 tasks
    LZ = sum(x['Z', j] for j in tasks)
    solver.Add(LZ >= 1)
    solver.Add(LZ <= 2)
    
    # Exactly one of X or Z takes 2 tasks => LX + LZ = 3
    solver.Add(LX + LZ == 3)
    
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        return solver.Objective().Value()
    else:
        return None

def solve_scenario_c():
    persons = ['X', 'Y', 'Z', 'R']
    tasks = ['A', 'B', 'C', 'D', 'F']
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    
    # Decision variables x[i][j]
    x = dict()
    for i in persons:
        for j in tasks:
            x[i, j] = solver.BoolVar('x_{}_{}'.format(i, j))
    
    # Cost coefficients
    cost = dict()
    cost[('X', 'A')] = 25
    cost[('X', 'B')] = 29
    cost[('X', 'C')] = 31
    cost[('X', 'D')] = 42
    cost[('X', 'F')] = 37
    cost[('Y', 'A')] = 39
    cost[('Y', 'B')] = 38
    cost[('Y', 'C')] = 26
    cost[('Y', 'D')] = 20
    cost[('Y', 'F')] = 33
    cost[('Z', 'A')] = 34
    cost[('Z', 'B')] = 27
    cost[('Z', 'C')] = 28
    cost[('Z', 'D')] = 40
    cost[('Z', 'F')] = 32
    cost[('R', 'A')] = 24
    cost[('R', 'B')] = 42
    cost[('R', 'C')] = 36
    cost[('R', 'D')] = 23
    cost[('R', 'F')] = 45
    
    # Objective: Minimize total cost
    obj_terms = []
    for i in persons:
        for j in tasks:
            obj_terms.append(cost[(i, j)] * x[i, j])
    solver.Minimize(sum(obj_terms))
    
    # Each person assigned exactly 1 task
    for i in persons:
        solver.Add(sum(x[i, j] for j in tasks) == 1)
    
    # Task A must be assigned
    solver.Add(sum(x[i, 'A'] for i in persons) == 1)
    
    # Task B must be assigned
    solver.Add(sum(x[i, 'B'] for i in persons) == 1)
    
    # Exactly two of C, D, F are assigned
    solver.Add(sum(x[i, 'C'] for i in persons) + sum(x[i, 'D'] for i in persons) + sum(x[i, 'F'] for i in persons) == 2)
    
    # Each task assigned to at most one person
    for j in tasks:
        solver.Add(sum(x[i, j] for i in persons) <= 1)
    
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        return solver.Objective().Value()
    else:
        return None

if __name__ == '__main__':
    # The problem asks to solve the model. Since there are three scenarios,
    # we solve all three and report their optimal values.
    # However, the output format requires a single OPTIMAL_VALUE line.
    # Given the ambiguity, we'll report the minimum across all scenarios as the primary answer,
    # but more likely the problem expects us to solve a specific one or all.
    # Let's solve all and print each, but the instruction says "single numeric result".
    # Re-reading: "The script must output ONLY the raw numeric result following the 'OPTIMAL_VALUE:' prefix"
    # and "the single numeric result the problem asks for".
    
    # Since the model presents three scenarios, and no specific scenario is singled out as THE problem,
    # but typically in such textbook problems, each part is separate. 
    # However, without further specification, I will solve all three and print the best (minimum) 
    # as a representative, OR more likely, the user wants to see the solution to the general model.
    
    # Actually, looking at the structure, it's likely three separate sub-problems.
    # Let's print the optimal values for each scenario clearly, but the guardrail says ONLY the result.
    # I will print the optimal value for scenario (a) as it is the first and most general "one person takes two" case.
    # But to be safe and useful, let's check if there's a standard interpretation.
    # Usually, if multiple scenarios are given, they are separate exercises.
    # I will solve all three and print them on separate lines with labels? No, "ONLY the raw numeric result".
    
    # Let's assume the question implies solving the model as defined. Since it has variants,
    # I will solve all three and print the minimum, which is the best possible outcome across all valid configurations.
    
    val_a = solve_scenario_a()
    val_b = solve_scenario_b()
    val_c = solve_scenario_c()
    
    results = []
    if val_a is not None:
        results.append(val_a)
    if val_b is not None:
        results.append(val_b)
    if val_c is not None:
        results.append(val_c)
    
    if results:
        print("OPTIMAL_VALUE:", min(results))
    else:
        print("NO_FEASIBLE_SOLUTION")