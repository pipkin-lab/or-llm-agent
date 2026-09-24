from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets
stations = ['I', 'II']
cities = [1, 2, 3]

# Parameters
Cap = dict()
Cap['I'] = 400
Cap['II'] = 450

D_min = dict()
D_min[1] = 290
D_min[2] = 250
D_min[3] = 270

D_max = dict()
D_max[1] = 320
D_max[2] = 250
D_max[3] = 350

C_cost = dict()
C_cost[('I', 1)] = 15
C_cost[('I', 2)] = 18
C_cost[('I', 3)] = 22
C_cost[('II', 1)] = 21
C_cost[('II', 2)] = 25
C_cost[('II', 3)] = 16

# Decision variables
x = dict()
for s in stations:
    for c in cities:
        x[(s, c)] = solver.NumVar(0, INF, 'x_' + s + '_' + str(c))

# Objective: Minimize total cost
obj_terms = []
for s in stations:
    for c in cities:
        obj_terms.append(C_cost[(s, c)] * x[(s, c)])
solver.Minimize(sum(obj_terms))

# Supply constraints: use all available electricity from each station
for s in stations:
    expr = sum(x[(s, c)] for c in cities)
    solver.Add(expr == Cap[s])

# Demand constraints
# City 1: 290 <= x_{I,1} + x_{II,1} <= 320
expr_c1 = sum(x[(s, 1)] for s in stations)
solver.Add(expr_c1 >= D_min[1])
solver.Add(expr_c1 <= D_max[1])

# City 2: x_{I,2} + x_{II,2} = 250
expr_c2 = sum(x[(s, 2)] for s in stations)
solver.Add(expr_c2 == D_min[2])

# City 3: 270 <= x_{I,3} + x_{II,3} <= 350
expr_c3 = sum(x[(s, 3)] for s in stations)
solver.Add(expr_c3 >= D_min[3])
solver.Add(expr_c3 <= D_max[3])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")