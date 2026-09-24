from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

x_I = solver.NumVar(0, INF, 'x_I')
x_II = solver.NumVar(0, INF, 'x_II')

# Material A: 1*x_I + 2*x_II <= 6000
solver.Add(x_I + 2 * x_II <= 6000, 'mat_A')

# Material B: 2*x_I + 1*x_II <= 8000
solver.Add(2 * x_I + x_II <= 8000, 'mat_B')

# Market cap on Product II
solver.Add(x_II <= 2, 'cap_II')

# II does not exceed I by more than 1: -x_I + x_II <= 1
solver.Add(-x_I + x_II <= 1, 'diff')

# Maximize wholesale revenue
solver.Maximize(30 * x_I + 20 * x_II)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")