from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index set
machines = ['A', 'B', 'C', 'D']

# Parameters
setup_cost = dict()
setup_cost['A'] = 1000
setup_cost['B'] = 920
setup_cost['C'] = 800
setup_cost['D'] = 700

unit_cost = dict()
unit_cost['A'] = 20
unit_cost['B'] = 24
unit_cost['C'] = 16
unit_cost['D'] = 28

capacity = dict()
capacity['A'] = 900
capacity['B'] = 1000
capacity['C'] = 1200
capacity['D'] = 1600

total_demand = 2000

# Decision variables
x = dict()
y = dict()
for i in machines:
    x[i] = solver.NumVar(0, INF, 'x_' + i)
    y[i] = solver.BoolVar('y_' + i)

# Objective function
obj_expr = 0
for i in machines:
    obj_expr += setup_cost[i] * y[i] + unit_cost[i] * x[i]
solver.Minimize(obj_expr)

# Demand satisfaction constraint
solver.Add(sum(x[i] for i in machines) == total_demand)

# Capacity / linking constraints
for i in machines:
    solver.Add(x[i] <= capacity[i] * y[i])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")