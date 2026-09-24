from ortools.linear_solver import pywraplp

# Define index set and parameters
machines = ['A', 'B', 'C', 'D']
S = dict()
S['A'] = 1000
S['B'] = 920
S['C'] = 800
S['D'] = 700
c = dict()
c['A'] = 20
c['B'] = 24
c['C'] = 16
c['D'] = 28
U = dict()
U['A'] = 900
U['B'] = 1000
U['C'] = 1200
U['D'] = 1600
D = 2000

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
y = dict()
for i in machines:
    x[i] = solver.NumVar(0, INF, 'x_' + i)
    y[i] = solver.BoolVar('y_' + i)

# Objective function
obj_terms = []
for i in machines:
    obj_terms.append(S[i] * y[i] + c[i] * x[i])
solver.Minimize(sum(obj_terms))

# Demand satisfaction constraint
solver.Add(sum(x[i] for i in machines) == D)

# Capacity constraints linked to setup
for i in machines:
    solver.Add(x[i] <= U[i] * y[i])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")