from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
S = solver.NumVar(0, INF, 'S')
x_A = solver.NumVar(0, INF, 'x_A')
x_B = solver.NumVar(0, INF, 'x_B')
x_C = solver.NumVar(0, INF, 'x_C')
y1 = solver.NumVar(0, INF, 'y1')
y2 = solver.NumVar(0, INF, 'y2')
y3 = solver.NumVar(0, INF, 'y3')
y4 = solver.NumVar(0, INF, 'y4')

# Constraint 1: Year 1 (2003) Balance
solver.Add(S - x_A - x_B - y1 >= 100)

# Constraint 2: Year 2 (2004) Balance
solver.Add(1.04 * y1 - x_C - y2 >= 150)

# Constraint 3: Year 3 (2005) Balance
solver.Add(1.04 * y2 + 1.25 * x_B - y3 >= 120)

# Constraint 4: Year 4 (2006) Balance
solver.Add(1.04 * y3 + 1.40 * x_A + 1.30 * x_C - y4 >= 110)

# Investment Limits
solver.Add(x_A <= 60)
solver.Add(x_B <= 90)
solver.Add(x_C <= 50)

# Objective: Minimize S
solver.Minimize(S)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")