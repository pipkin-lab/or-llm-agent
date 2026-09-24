from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define index sets
I = range(5)  # Athletes: 1 to 5
J = range(4)  # Strokes: 1 to 4

# Parameters: c[i][j] is the time for athlete i in stroke j
# Data from the table
c = dict()
# Stroke 1 (Backstroke)
c[(1, 0)] = 37.7
c[(2, 0)] = 32.9
c[(3, 0)] = 33.8
c[(4, 0)] = 37.0
c[(5, 0)] = 35.4
# Stroke 2 (Breaststroke)
c[(1, 1)] = 43.4
c[(2, 1)] = 33.1
c[(3, 1)] = 42.2
c[(4, 1)] = 34.7
c[(5, 1)] = 41.8
# Stroke 3 (Butterfly)
c[(1, 2)] = 33.3
c[(2, 2)] = 28.5
c[(3, 2)] = 38.9
c[(4, 2)] = 30.4
c[(5, 2)] = 33.6
# Stroke 4 (Freestyle)
c[(1, 3)] = 29.2
c[(2, 3)] = 26.4
c[(3, 3)] = 29.6
c[(4, 3)] = 28.5
c[(5, 3)] = 31.1

# Decision Variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective Function
obj = 0
for i in I:
    for j in J:
        obj += c[i, j] * x[i, j]

solver.Minimize(obj)

# Constraints

# 1. Each stroke must be assigned to exactly one athlete
for j in J:
    solver.Add(sum(x[i, j] for i in I) == 1)

# 2. Each athlete can be assigned to at most one stroke
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")