from ortools.linear_solver import pywraplp

# Define the problem
workers = ['A', 'B', 'C', 'D', 'E']
stations = ['I', 'II', 'III', 'IV', 'V']

# Efficiency matrix E[i][j]
E = dict()
E[('A', 'I')] = 2
E[('A', 'II')] = 3
E[('A', 'III')] = 4
E[('A', 'IV')] = 1
E[('A', 'V')] = 7
E[('B', 'I')] = 3
E[('B', 'II')] = 4
E[('B', 'III')] = 2
E[('B', 'IV')] = 5
E[('B', 'V')] = 6
E[('C', 'I')] = 2
E[('C', 'II')] = 5
E[('C', 'III')] = 3
E[('C', 'IV')] = 4
E[('C', 'V')] = 1
E[('D', 'I')] = 5
E[('D', 'II')] = 2
E[('D', 'III')] = 3
E[('D', 'IV')] = 2
E[('D', 'V')] = 5
E[('E', 'I')] = 3
E[('E', 'II')] = 7
E[('E', 'III')] = 6
E[('E', 'IV')] = 2
E[('E', 'V')] = 4

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x = dict()
for i in workers:
    for j in stations:
        x[(i, j)] = solver.BoolVar('x_' + i + '_' + j)

Z = solver.NumVar(0, solver.infinity(), 'Z')

# Objective: Maximize Z
solver.Maximize(Z)

# Constraint 1: Each worker assigned to exactly one station
for i in workers:
    solver.Add(sum(x[(i, j)] for j in stations) == 1)

# Constraint 2: Each station assigned exactly one worker
for j in stations:
    solver.Add(sum(x[(i, j)] for i in workers) == 1)

# Constraint 3: Bottleneck definition
for j in stations:
    solver.Add(sum(E[(i, j)] * x[(i, j)] for i in workers) >= Z)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")