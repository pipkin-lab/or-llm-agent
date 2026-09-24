from ortools.linear_solver import pywraplp

# Define the problem
solver = pywraplp.Solver.CreateSolver('GLOP')

# Nodes
nodes = ['X', 'Y', 'A', 'B', 'C']
n = len(nodes)

# Supply and Demand
supply = {'X': 70, 'Y': 55}
demand = {'A': 35, 'B': 40, 'C': 50}

# Distances c[i][j]
dist = {}
for i in nodes:
    for j in nodes:
        if i == j:
            dist[i][j] = 0
        else:
            dist[i][j] = None

# Fill in distances
dist['X']['Y'] = 12
dist['Y']['X'] = 10
dist['X']['A'] = 10
dist['X']['B'] = 14
dist['X']['C'] = 12
dist['Y']['A'] = 15
dist['Y']['B'] = 12
dist['Y']['C'] = 18
dist['A']['B'] = 14
dist['A']['C'] = 11
dist['B']['A'] = 10
dist['B']['C'] = 4
dist['C']['A'] = 8
dist['C']['B'] = 12

# Decision variables x[i][j] for all i != j
x = dict()
for i in nodes:
    for j in nodes:
        if i != j:
            x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + i + '_' + j)

# Objective function: Minimize total transport distance
obj_terms = []
for i in nodes:
    for j in nodes:
        if i != j:
            obj_terms.append(dist[i][j] * x[i, j])

solver.Minimize(sum(obj_terms))

# Flow conservation constraints
for i in nodes:
    outflow = sum(x[i, j] for j in nodes if j != i)
    inflow = sum(x[k, i] for k in nodes if k != i)
    
    if i in supply:
        solver.Add(outflow - inflow == supply[i])
    elif i in demand:
        solver.Add(outflow - inflow == -demand[i])

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")