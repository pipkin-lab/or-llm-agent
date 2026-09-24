from ortools.linear_solver import pywraplp

# Define swimmers and strokes
swimmers = ['Z', 'Q', 'Zh', 'W', 'Jo']
strokes = ['Back', 'Breast', 'Butt', 'Free']

# Cost matrix c[i][j]
c = dict()
c[('Z', 'Back')] = 37.7
c[('Z', 'Breast')] = 43.4
c[('Z', 'Butt')] = 33.3
c[('Z', 'Free')] = 29.2
c[('Q', 'Back')] = 32.9
c[('Q', 'Breast')] = 33.1
c[('Q', 'Butt')] = 28.5
c[('Q', 'Free')] = 26.4
c[('Zh', 'Back')] = 33.8
c[('Zh', 'Breast')] = 42.2
c[('Zh', 'Butt')] = 38.9
c[('Zh', 'Free')] = 29.6
c[('W', 'Back')] = 37.0
c[('W', 'Breast')] = 34.7
c[('W', 'Butt')] = 30.4
c[('W', 'Free')] = 28.5
c[('Jo', 'Back')] = 35.4
c[('Jo', 'Breast')] = 41.8
c[('Jo', 'Butt')] = 33.6
c[('Jo', 'Free')] = 31.1

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Create binary decision variables x[i, j]
x = dict()
for i in swimmers:
    for j in strokes:
        x[i, j] = solver.BoolVar('x_' + i + '_' + j)

# Objective: Minimize total time
objective = 0
for i in swimmers:
    for j in strokes:
        objective += c[(i, j)] * x[i, j]

solver.Minimize(objective)

# Stroke coverage constraints: each stroke assigned to exactly one swimmer
for j in strokes:
    solver.Add(sum(x[i, j] for i in swimmers) == 1)

# Swimmer assignment constraints: each swimmer assigned to at most one stroke
for i in swimmers:
    solver.Add(sum(x[i, j] for j in strokes) <= 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")