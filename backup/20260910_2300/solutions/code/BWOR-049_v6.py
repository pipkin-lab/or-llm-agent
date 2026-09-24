from ortools.linear_solver import pywraplp

# Define solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Node set
nodes = ['X', 'Y', 'A', 'B', 'C']

# Net balance (positive = supply, negative = demand)
b = dict()
b['X'] = 70
b['Y'] = 55
b['A'] = -35
b['B'] = -40
b['C'] = -50

# Arc set and costs
arcs = [
    ('X', 'Y'), ('Y', 'X'),
    ('X', 'A'), ('X', 'B'), ('X', 'C'),
    ('Y', 'A'), ('Y', 'B'), ('Y', 'C'),
    ('A', 'B'), ('A', 'C'),
    ('B', 'A'), ('B', 'C'),
    ('C', 'A'), ('C', 'B')
]

# Cost dictionary
c = dict()
c[('X', 'Y')] = 12
c[('Y', 'X')] = 10
c[('X', 'A')] = 10
c[('X', 'B')] = 14
c[('X', 'C')] = 12
c[('Y', 'A')] = 15
c[('Y', 'B')] = 12
c[('Y', 'C')] = 18
c[('A', 'B')] = 14
c[('A', 'C')] = 11
c[('B', 'A')] = 10
c[('B', 'C')] = 4
c[('C', 'A')] = 8
c[('C', 'B')] = 12

# Decision variables
x = dict()
for i, j in arcs:
    x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + i + '_' + j)

# Objective: minimize total cost
obj_terms = []
for i, j in arcs:
    obj_terms.append(c[(i, j)] * x[i, j])
solver.Minimize(sum(obj_terms))

# Flow conservation constraints for each node
for node in nodes:
    # Outgoing flow
    out_terms = []
    for i, j in arcs:
        if i == node:
            out_terms.append(x[i, j])
    # Incoming flow
    in_terms = []
    for i, j in arcs:
        if j == node:
            in_terms.append(x[i, j])
    
    # Flow conservation: sum(out) - sum(in) = b[node]
    if out_terms and in_terms:
        expr = sum(out_terms) - sum(in_terms)
    elif out_terms:
        expr = sum(out_terms)
    elif in_terms:
        expr = -sum(in_terms)
    else:
        expr = 0
    
    solver.Add(expr == b[node])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")