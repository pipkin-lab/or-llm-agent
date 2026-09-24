from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    raise ValueError("Could not create solver")

I = ['A', 'B', 'C']
J = ['X', 'Y', 'Z']

supply = dict()
supply['A'] = 1000
supply['B'] = 2000
supply['C'] = 2000

demand = dict()
for i in I:
    for j in J:
        demand[i, j] = 1500

profit = dict()
profit['A', 'X'] = 5
profit['A', 'Y'] = 4
profit['A', 'Z'] = 0
profit['B', 'X'] = 16
profit['B', 'Y'] = 8
profit['B', 'Z'] = 6
profit['C', 'X'] = 12
profit['C', 'Y'] = 10
profit['C', 'Z'] = 11

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + i + '_' + j)

obj = sum(profit[i, j] * x[i, j] for i in I for j in J)
solver.Maximize(obj)

for i in I:
    solver.Add(sum(x[i, j] for j in J) <= supply[i])

for i in I:
    for j in J:
        solver.Add(x[i, j] <= demand[i, j])

solver.Add(x['C', 'Z'] >= 1000)
solver.Add(x['A', 'Z'] == 0)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")