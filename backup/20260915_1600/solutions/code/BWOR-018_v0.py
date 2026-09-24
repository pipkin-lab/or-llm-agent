from ortools.linear_solver import pywraplp

# Define index sets (1-indexed)
I = [1, 2, 3, 4, 5]
J = [1, 2, 3, 4, 5]

# Cost matrix c[i][j]
cost = dict()
cost[1, 1] = 4
cost[1, 2] = 8
cost[1, 3] = 7
cost[1, 4] = 15
cost[1, 5] = 12
cost[2, 1] = 7
cost[2, 2] = 9
cost[2, 3] = 17
cost[2, 4] = 14
cost[2, 5] = 10
cost[3, 1] = 6
cost[3, 2] = 9
cost[3, 3] = 12
cost[3, 4] = 8
cost[3, 5] = 7
cost[4, 1] = 6
cost[4, 2] = 7
cost[4, 3] = 14
cost[4, 4] = 6
cost[4, 5] = 10
cost[5, 1] = 6
cost[5, 2] = 9
cost[5, 3] = 12
cost[5, 4] = 10
cost[5, 5] = 6

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[i, j]
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: minimize total cost
obj = sum(cost[i, j] * x[i, j] for i in I for j in J)
solver.Minimize(obj)

# Constraint 1: Each store assigned to exactly one company
for j in J:
    solver.Add(sum(x[i, j] for i in I) == 1)

# Constraint 2: Each company assigned to exactly one store
for i in I:
    solver.Add(sum(x[i, j] for j in J) == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")