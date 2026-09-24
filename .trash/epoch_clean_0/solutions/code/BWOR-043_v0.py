from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
I = range(1, 5)  # Origins: 1 to 4
J = range(1, 7)  # Destinations: 1 to 6

# Supply capacities
S = dict()
S[1] = 50
S[2] = 40
S[3] = 60
S[4] = 31

# Demand requirements
D = dict()
D[1] = 30
D[2] = 50
D[3] = 20
D[4] = 40
D[5] = 30
D[6] = 11

# Unit transportation costs C[i][j]
C = dict()
# Row 1 (A1)
C[1, 1] = 2
C[1, 2] = 1
C[1, 3] = 3
C[1, 4] = 3
C[1, 5] = 3
C[1, 6] = 5
# Row 2 (A2)
C[2, 1] = 4
C[2, 2] = 2
C[2, 3] = 2
C[2, 4] = 4
C[2, 5] = 4
C[2, 6] = 4
# Row 3 (A3)
C[3, 1] = 3
C[3, 2] = 5
C[3, 3] = 4
C[3, 4] = 2
C[3, 5] = 4
C[3, 6] = 1
# Row 4 (A4)
C[4, 1] = 4
C[4, 2] = 2
C[4, 3] = 2
C[4, 4] = 1
C[4, 5] = 2
C[4, 6] = 2

# Decision variables x[i, j]
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

# Objective function: Minimize total cost
obj = 0
for i in I:
    for j in J:
        obj += C[i, j] * x[i, j]

solver.Minimize(obj)

# Supply constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) == S[i])

# Demand constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")