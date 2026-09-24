from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Decision variables
x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')
x3 = solver.NumVar(0, solver.infinity(), 'x3')
T = solver.NumVar(0, solver.infinity(), 'T')

# Constraints
# Raw material: 10*x1 + 40*x2 + 80*x3 <= 90000
solver.Add(10 * x1 + 40 * x2 + 80 * x3 <= 90000)

# Labor: x1 + x2 + x3 - 30*T <= 3000
solver.Add(x1 + x2 + x3 - 30 * T <= 3000)

# Objective: Maximize 2*x1 + 3*x2 + 1*x3 - 40*T
solver.Maximize(2 * x1 + 3 * x2 + 1 * x3 - 40 * T)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")