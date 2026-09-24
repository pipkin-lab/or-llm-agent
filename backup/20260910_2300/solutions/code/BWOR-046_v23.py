from ortools.linear_solver import pywraplp

# Define index sets
I = ['A1', 'A2', 'A3']
J = ['B1', 'B2', 'B3', 'B4', 'B5']

# Parameters
factory_capacity = 270
warehouse_capacity = dict()
warehouse_capacity['A1'] = 50
warehouse_capacity['A2'] = 100
warehouse_capacity['A3'] = 150

demand = dict()
demand['B1'] = 25
demand['B2'] = 105
demand['B3'] = 60
demand['B4'] = 30
demand['B5'] = 70

# Cost matrix c_ij
cost = dict()
cost[('A1', 'B1')] = 10
cost[('A1', 'B2')] = 15
cost[('A1', 'B3')] = 20
cost[('A1', 'B4')] = 20
cost[('A1', 'B5')] = 40
cost[('A2', 'B1')] = 20
cost[('A2', 'B2')] = 40
cost[('A2', 'B3')] = 15
cost[('A2', 'B4')] = 30
cost[('A2', 'B5')] = 30
cost[('A3', 'B1')] = 30
cost[('A3', 'B2')] = 35
cost[('A3', 'B3')] = 40
cost[('A3', 'B4')] = 55
cost[('A3', 'B5')] = 25

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
# x[i][j]: amount shipped from warehouse i to region j
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# y[i]: amount received by warehouse i from factory
y = dict()
for i in I:
    y[i] = solver.NumVar(0, INF, 'y_' + i)

# Objective: minimize total cost
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(cost[(i, j)] * x[i, j])
solver.Minimize(sum(obj_terms))

# Constraint 1: Factory supply limit
solver.Add(sum(y[i] for i in I) <= factory_capacity)

# Constraint 2: Warehouse flow conservation and capacity
for i in I:
    # y_i = sum_j x_ij
    solver.Add(y[i] == sum(x[i, j] for j in J))
    # sum_j x_ij <= C_i
    solver.Add(sum(x[i, j] for j in J) <= warehouse_capacity[i])

# Constraint 3: Regional demand constraints (demand is upper-bounded)
for j in J:
    solver.Add(sum(x[i, j] for i in I) <= demand[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")