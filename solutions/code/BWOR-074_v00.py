from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

grades = ['A', 'B', 'C', 'D', 'E']
positions = [1, 2, 3, 4, 5]

n = dict()
n['A'] = 5000
n['B'] = 12500
n['C'] = 15000
n['D'] = 10000
n['E'] = 7500

x = dict()
for g in grades:
    for k in positions:
        x[g, k] = solver.BoolVar('x_' + g + '_' + str(k))

for g in grades:
    solver.Add(sum(x[g, k] for k in positions) == 1)

for k in positions:
    solver.Add(sum(x[g, k] for g in grades) == 1)

obj = sum(n[g] * k * x[g, k] for g in grades for k in positions)
solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")