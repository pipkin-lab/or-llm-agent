from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Define arcs
arcs = [
    ('X', 'Y'), ('Y', 'X'),
    ('X', 'A'), ('X', 'B'), ('X', 'C'),
    ('Y', 'A'), ('Y', 'B'), ('Y', 'C'),
    ('A', 'B'), ('A', 'C'),
    ('B', 'A'), ('B', 'C'),
    ('C', 'A'), ('C', 'B')
]

# Distances
dist = dict()
dist['X', 'Y'] = 12
dist['Y', 'X'] = 10
dist['X', 'A'] = 10
dist['X', 'B'] = 14
dist['X', 'C'] = 12
dist['Y', 'A'] = 15
dist['Y', 'B'] = 12
dist['Y', 'C'] = 18
dist['A', 'B'] = 14
dist['A', 'C'] = 11
dist['B', 'A'] = 10
dist['B', 'C'] = 4
dist['C', 'A'] = 8
dist['C', 'B'] = 12

# Supply and Demand
supply = dict()
supply['X'] = 70
supply['Y'] = 55
supply['A'] = 0
supply['B'] = 0
supply['C'] = 0

demand = dict()
demand['X'] = 0
demand['Y'] = 0
demand['A'] = 35
demand['B'] = 40
demand['C'] = 50

nodes = ['X', 'Y', 'A', 'B', 'C']

# Decision variables
x = dict()
for i, j in arcs:
    x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# Objective: minimize total distance
obj = 0
for i, j in arcs:
    obj += dist[i, j] * x[i, j]
solver.Minimize(obj)

# Flow balance constraints for each node
for k in nodes:
    inflow = 0
    outflow = 0
    for i, j in arcs:
        if j == k:
            inflow += x[i, j]
        if i == k:
            outflow += x[i, j]
    solver.Add(outflow - inflow == supply[k] - demand[k])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")