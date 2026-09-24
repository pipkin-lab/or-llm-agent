from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

machines = ['A', 'B', 'C', 'D']

fixed_costs = dict()
fixed_costs['A'] = 1000
fixed_costs['B'] = 920
fixed_costs['C'] = 800
fixed_costs['D'] = 700

unit_costs = dict()
unit_costs['A'] = 20
unit_costs['B'] = 24
unit_costs['C'] = 16
unit_costs['D'] = 28

capacities = dict()
capacities['A'] = 900
capacities['B'] = 1000
capacities['C'] = 1200
capacities['D'] = 1600

x = dict()
y = dict()

for i in machines:
    x[i] = solver.NumVar(0, INF, 'x_' + i)
    y[i] = solver.BoolVar('y_' + i)

obj = 0
for i in machines:
    obj += fixed_costs[i] * y[i] + unit_costs[i] * x[i]

solver.Minimize(obj)

solver.Add(sum(x[i] for i in machines) == 2000)

for i in machines:
    solver.Add(x[i] <= capacities[i])
    solver.Add(x[i] <= capacities[i] * y[i])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")