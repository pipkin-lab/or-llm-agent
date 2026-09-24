from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

INF = solver.infinity()

x1 = solver.IntVar(0, INF, 'x1')
x2 = solver.IntVar(0, INF, 'x2')
x3 = solver.IntVar(0, INF, 'x3')

solver.Add(2 * x1 + 3 * x2 + 4 * x3 <= 10)

solver.Maximize(100 * x1 + 140 * x2 + 180 * x3)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")