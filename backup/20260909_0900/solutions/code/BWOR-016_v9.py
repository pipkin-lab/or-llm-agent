from ortools.linear_solver import pywraplp

# Define the solver (MILP because of binary variables)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
I = ['A1', 'A2', 'A3', 'A4']
J = ['B1', 'B2', 'B3', 'B4']
K = ['A3', 'A4']

# Parameters
S = {'A1': 400, 'A2': 600, 'A3': 200, 'A4': 200}
D = {'B1': 350, 'B2': 400, 'B3': 300, 'B4': 150}

c = {
    ('A1', 'B1'): 2, ('A1', 'B2'): 9, ('A1', 'B3'): 3, ('A1', 'B4'): 4,
    ('A2', 'B1'): 8, ('A2', 'B2'): 3, ('A2', 'B3'): 5, ('A2', 'B4'): 7,
    ('A3', 'B1'): 7, ('A3', 'B2'): 6, ('A3', 'B3'): 1, ('A3', 'B4'): 2,
    ('A4', 'B1'): 4, ('A4', 'B2'): 5, ('A4', 'B3'): 2, ('A4', 'B4'): 5,
}

F = {'A3': 1200, 'A4': 1500}

# Decision Variables
# x[i][j] >= 0 continuous
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + i + '_' + j)

# y[k] binary
y = dict()
for k in K:
    y[k] = solver.BoolVar('y_' + k)

# Objective Function
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(c[(i, j)] * x[i, j])
for k in K:
    obj_terms.append(F[k] * y[k])

solver.Minimize(sum(obj_terms))

# Constraints

# 1. Demand satisfaction
for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

# 2. Production capacity
# Existing factories A1, A2
for i in ['A1', 'A2']:
    solver.Add(sum(x[i, j] for j in J) <= S[i])

# New factories A3, A4
for k in K:
    solver.Add(sum(x[k, j] for j in J) <= S[k] * y[k])

# 3. Exactly one new factory
solver.Add(y['A3'] + y['A4'] == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")