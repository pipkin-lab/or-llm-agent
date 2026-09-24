from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Index sets (1-indexed as per model)
I = [1, 2, 3]
J = [1, 2, 3, 4, 5]

# Parameters
S = dict()
S[1] = 50
S[2] = 100
S[3] = 150

D = dict()
D[1] = 25
D[2] = 115
D[3] = 60
D[4] = 30
D[5] = 70

C = dict()
# Row i, column j
C[(1, 1)] = 10
C[(1, 2)] = 15
C[(1, 3)] = 20
C[(1, 4)] = 20
C[(1, 5)] = 40
C[(2, 1)] = 20
C[(2, 2)] = 10
C[(2, 3)] = 15
C[(2, 4)] = 30
C[(2, 5)] = 30
C[(3, 1)] = 30
C[(3, 2)] = 35
C[(3, 3)] = 40
C[(3, 4)] = 55
C[(3, 5)] = 25

# Decision variables
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

# Objective
obj = 0
for i in I:
    for j in J:
        obj += C[(i, j)] * x[i, j]
solver.Minimize(obj)

# Supply constraints
for i in I:
    expr = sum(x[i, j] for j in J)
    solver.Add(expr == S[i])

# Demand constraints
for j in J:
    expr = sum(x[i, j] for i in I)
    solver.Add(expr == D[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")