from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    raise RuntimeError("Failed to create solver")

# Define nodes
nodes = ['X', 'Y', 'A', 'B', 'C']

# Define supply and demand
supply = {'X': 70, 'Y': 55, 'A': 0, 'B': 0, 'C': 0}
demand = {'X': 0, 'Y': 0, 'A': 35, 'B': 40, 'C': 50}

# Define distances (arcs)
# x_{u,v} is flow from u to v
distances = {
    ('X', 'Y'): 12,
    ('X', 'A'): 10,
    ('X', 'B'): 14,
    ('X', 'C'): 12,
    ('Y', 'X'): 10,
    ('Y', 'A'): 15,
    ('Y', 'B'): 12,
    ('Y', 'C'): 18,
    ('A', 'B'): 14,
    ('A', 'C'): 11,
    ('B', 'A'): 10,
    ('B', 'C'): 4,
    ('C', 'A'): 8,
    ('C', 'B'): 12
}

# Create decision variables
x = dict()
for (u, v) in distances:
    x[u, v] = solver.NumVar(0, solver.infinity(), 'x_' + u + '_' + v)

# Objective function: Minimize total transportation distance
obj_terms = []
for (u, v) in distances:
    obj_terms.append(distances[(u, v)] * x[u, v])

solver.Minimize(sum(obj_terms))

# Flow balance constraints for each node
# General form: sum(inflow) + supply[u] == sum(outflow) + demand[u]
# Rearranged: sum(outflow) - sum(inflow) == supply[u] - demand[u]

for u in nodes:
    # Calculate net supply (supply - demand)
    net_supply = supply[u] - demand[u]
    
    # Build the flow balance expression: sum(outflow) - sum(inflow)
    flow_expr = 0
    for (a, b) in distances:
        if a == u:
            # Outflow from u to b
            flow_expr += x[a, b]
        if b == u:
            # Inflow from a to u
            flow_expr -= x[a, b]
    
    # Constraint: sum(outflow) - sum(inflow) == net_supply
    solver.Add(flow_expr == net_supply)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")