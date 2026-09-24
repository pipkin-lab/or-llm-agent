from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

x1 = solver.NumVar(0, INF, 'x1')
x2 = solver.NumVar(0, INF, 'x2')
x3 = solver.NumVar(0, INF, 'x3')

obj = 2 * x1 + 3 * x2 + 1 * x3
solver.Maximize(obj)

solver.Add(x1 + x2 + x3 <= 3000)
solver.Add(x1 + 4 * x2 + 8 * x3 <= 9000)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")