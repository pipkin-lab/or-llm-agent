from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

K = solver.NumVar(0, INF, 'K')
x_A = solver.NumVar(0, 60, 'x_A')
x_B = solver.NumVar(0, 90, 'x_B')
x_C = solver.NumVar(0, 50, 'x_C')
S_3 = solver.NumVar(0, INF, 'S_3')
S_4 = solver.NumVar(0, INF, 'S_4')
S_5 = solver.NumVar(0, INF, 'S_5')
S_6 = solver.NumVar(0, INF, 'S_6')

# Constraint 1: Year 2003
solver.Add(K - x_A - S_3 == 100)

# Constraint 2: Year 2004
solver.Add(1.04 * S_3 - x_B - x_C - S_4 == 150)

# Constraint 3: Year 2005
solver.Add(1.04 * S_4 + 1.40 * x_A + 1.25 * x_B + 1.30 * x_C - S_5 == 120)

# Constraint 4: Year 2006
solver.Add(1.04 * S_5 - S_6 == 110)

solver.Minimize(K)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")