from ortools.linear_solver import pywraplp

# Define index sets
plants = ['A', 'B', 'C', 'D']
regions = ['I', 'II', 'III', 'IV', 'V', 'VI']

# Parameters
supply = {'A': 200, 'B': 300, 'C': 400, 'D': 100}
demand = {'I': 200, 'II': 150, 'III': 400, 'IV': 100, 'V': 150, 'VI': 150}
prod_cost = {'A': 1.2, 'B': 1.4, 'C': 1.1, 'D': 1.5}
sales_price = {'I': 2.0, 'II': 2.4, 'III': 1.8, 'IV': 2.2, 'V': 1.6, 'VI': 2.0}

# Transport cost matrix (yuan/kg)
transport_cost = dict()
transport_cost['A', 'I'] = 0.5
transport_cost['A', 'II'] = 0.4
transport_cost['A', 'III'] = 0.3
transport_cost['A', 'IV'] = 0.4
transport_cost['A', 'V'] = 0.3
transport_cost['A', 'VI'] = 0.1
transport_cost['B', 'I'] = 0.3
transport_cost['B', 'II'] = 0.8
transport_cost['B', 'III'] = 0.9
transport_cost['B', 'IV'] = 0.5
transport_cost['B', 'V'] = 0.6
transport_cost['B', 'VI'] = 0.2
transport_cost['C', 'I'] = 0.7
transport_cost['C', 'II'] = 0.7
transport_cost['C', 'III'] = 0.3
transport_cost['C', 'IV'] = 0.7
transport_cost['C', 'V'] = 0.4
transport_cost['C', 'VI'] = 0.4
transport_cost['D', 'I'] = 0.6
transport_cost['D', 'II'] = 0.4
transport_cost['D', 'III'] = 0.2
transport_cost['D', 'IV'] = 0.6
transport_cost['D', 'V'] = 0.5
transport_cost['D', 'VI'] = 0.8

# Additional constraints
min_region_III = 100
region_IV_exact = 100

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables x[i][j]
x = dict()
for i in plants:
    for j in regions:
        x[i, j] = solver.NumVar(0, INF, 'x_' + i + '_' + j)

# Objective function: maximize total profit (yuan)
# pi[i][j] = 1000 * (sales_price[j] - prod_cost[i] - transport_cost[i][j])
obj_terms = []
for i in plants:
    for j in regions:
        pi = 1000 * (sales_price[j] - prod_cost[i] - transport_cost[i, j])
        obj_terms.append(pi * x[i, j])

solver.Maximize(sum(obj_terms))

# Supply constraints: sum_j x[i][j] = supply[i]
for i in plants:
    solver.Add(sum(x[i, j] for j in regions) == supply[i])

# Demand constraints
for j in regions:
    if j == 'IV':
        # Region IV must be fully satisfied
        solver.Add(sum(x[i, j] for i in plants) == region_IV_exact)
    else:
        # Other regions: demand is an upper bound
        solver.Add(sum(x[i, j] for i in plants) <= demand[j])

# Minimum supply to Region III
solver.Add(sum(x[i, 'III'] for i in plants) >= min_region_III)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")