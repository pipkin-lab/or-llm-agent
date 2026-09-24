from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

INF = solver.infinity()

x1 = solver.NumVar(0, INF, 'x1')
x2 = solver.NumVar(0, INF, 'x2')
x3 = solver.NumVar(0, INF, 'x3')
x4 = solver.NumVar(0, INF, 'x4')
x5 = solver.NumVar(0, INF, 'x5')

# Objective: Minimize cost
objective = 0.2 * x1 + 0.7 * x2 + 0.4 * x3 + 0.3 * x4 + 0.8 * x5
solver.Minimize(objective)

# Constraint 1: Protein >= 700
solver.Add(3 * x1 + 2 * x2 + 1 * x3 + 6 * x4 + 18 * x5 >= 700)

# Constraint 2: Minerals >= 30
solver.Add(1.0 * x1 + 0.5 * x2 + 0.2 * x3 + 2.0 * x4 + 0.5 * x5 >= 30)

# Constraint 3: Vitamins >= 100
solver.Add(0.5 * x1 + 1.0 * x2 + 0.2 * x3 + 2.0 * x4 + 0.8 * x5 >= 100)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")