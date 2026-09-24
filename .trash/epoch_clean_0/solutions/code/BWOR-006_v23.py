from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x1_A1 = solver.NumVar(0, INF, 'x1_A1')
x2_A1 = solver.NumVar(0, INF, 'x2_A1')
x1_A2 = solver.NumVar(0, INF, 'x1_A2')
x2_A2 = solver.NumVar(0, INF, 'x2_A2')
x3_A2 = solver.NumVar(0, INF, 'x3_A2')

x1_B1 = solver.NumVar(0, INF, 'x1_B1')
x2_B1 = solver.NumVar(0, INF, 'x2_B1')
x1_B2 = solver.NumVar(0, INF, 'x1_B2')
x3_B2 = solver.NumVar(0, INF, 'x3_B2')
x1_B3 = solver.NumVar(0, INF, 'x1_B3')

# Objective function
solver.Maximize(
    0.75 * x1_A1 + 1.15 * x2_A1 + 0.79 * x1_A2 + 1.38 * x2_A2 + 1.94 * x3_A2
    - 0.36 * x1_B1 - 0.48 * x2_B1 - 0.44 * x1_B2 - 1.21 * x3_B2 - 0.35 * x1_B3
)

# Flow Balance Constraints
solver.Add(x1_B1 + x1_B2 + x1_B3 == x1_A1 + x1_A2)
solver.Add(x2_B1 == x2_A1 + x2_A2)
solver.Add(x3_B2 == x3_A2)

# Machine Capacity Constraints
solver.Add(5 * x1_A1 + 10 * x2_A1 <= 6000)
solver.Add(7 * x1_A2 + 9 * x2_A2 + 12 * x3_A2 <= 10000)
solver.Add(6 * x1_B1 + 8 * x2_B1 <= 4000)
solver.Add(4 * x1_B2 + 11 * x3_B2 <= 7000)
solver.Add(7 * x1_B3 <= 4000)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")