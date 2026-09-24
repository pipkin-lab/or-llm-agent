from ortools.linear_solver import pywraplp

# Parameters
p = {1: 0.3, 2: 0.5, 3: 0.2}
scores = [1, 2, 3]

# Generate all 64 possible strategies
# A strategy is defined by (x11, x12, x13, x21, x22, x23)
strategies = []
for x11 in [0, 1]:
    for x12 in [0, 1]:
        for x13 in [0, 1]:
            for x21 in [0, 1]:
                for x22 in [0, 1]:
                    for x23 in [0, 1]:
                        strategies.append((x11, x12, x13, x21, x22, x23))

# Pre-calculate Z_m for each strategy m
Z_values = []
for m in strategies:
    x11, x12, x13, x21, x22, x23 = m
    # x1[k] is the decision to hire candidate 1 at score k
    x1 = {1: x11, 2: x12, 3: x13}
    # x2[k] is the decision to hire candidate 2 at score k
    x2 = {1: x21, 2: x22, 3: x23}
    
    # R1: Probability of rejecting C1
    R1 = sum(p[k] * (1 - x1[k]) for k in scores)
    
    # R2: Probability of rejecting C2 (conditional on reaching C2)
    R2 = sum(p[k] * (1 - x2[k]) for k in scores)
    
    # Expected score if hiring C1
    E_hire_1 = sum(p[k] * x1[k] * k for k in scores)
    
    # Expected score if reaching C2 and hiring C2
    E_hire_2 = sum(p[k] * x2[k] * k for k in scores)
    
    # Expected score of C3
    E_score_3 = sum(p[k] * k for k in scores)
    
    # Total Expected Score Z_m
    Z_m = E_hire_1 + R1 * E_hire_2 + R1 * R2 * E_score_3
    Z_values.append(Z_m)

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    print("No SCIP solver available, trying GLOP (though this is a binary problem)")
    solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables y_m
y = dict()
for i in range(len(strategies)):
    y[i] = solver.IntVar(0, 1, 'y_' + str(i))

# Objective: Maximize Z
obj = sum(Z_values[i] * y[i] for i in range(len(strategies)))
solver.Maximize(obj)

# Constraint: Sum of y_m == 1
solver.Add(sum(y[i] for i in range(len(strategies))) == 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")