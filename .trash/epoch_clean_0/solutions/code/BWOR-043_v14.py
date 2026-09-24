from ortools.linear_solver import pywraplp

# Initialize LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Index sets
I = range(1, 5)   # Origins: 1, 2, 3, 4
J = range(1, 7)   # Destinations: 1, 2, 3, 4, 5, 6

# Supply
S = dict()
S[1] = 50
S[2] = 40
S[3] = 60
S[4] = 31

# Demand
D = dict()
D[1] = 30
D[2] = 50
D[3] = 20
D[4] = 40
D[5] = 30
D[6] = 11

# Unit transportation costs
C = dict()
C[1, 1] = 2
C[1, 2] = 1
C[1, 3] = 3
C[1, 4] = 3
C[1, 5] = 3
C[1, 6] = 5
C[2, 1] = 4
C[2, 2] = 2
C[2, 3] = 2
C[2, 4] = 4
C[2, 5] = 4
C[2, 6] = 4
C[3, 1] = 3
C[3, 2] = 5
C[3, 3] = 4
C[3, 4] = 2
C[3, 5] = 4
C[3, 6] = 1
C[4, 1] = 4
C[4, 2] = 2
C[4, 3] = 2
C[4, 4] = 1
C[4, 5] = 2
C[4, 6] = 2

# Decision variables: x[i, j] >= 0
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

# Objective: minimize total transportation cost
obj = sum(C[i, j] * x[i, j] for i in I for j in J)
solver.Minimize(obj)

# Supply constraints (equality)
for i in I:
    solver.Add(sum(x[i, j] for j in J) == S[i])

# Demand constraints (equality)
for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")