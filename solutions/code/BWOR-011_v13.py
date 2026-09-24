from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables x[i][j] for i in {1,2}, j in {1,2,3}
x = dict()
for i in [1, 2]:
    for j in [1, 2, 3]:
        x[i, j] = solver.NumVar(0, INF, 'x_{}{}'.format(i, j))

# Objective: minimize total cost
objective = (
    15 * x[1, 1] + 18 * x[1, 2] + 22 * x[1, 3]
    + 21 * x[2, 1] + 25 * x[2, 2] + 16 * x[2, 3]
)
solver.Minimize(objective)

# Supply constraints (equality)
solver.Add(x[1, 1] + x[1, 2] + x[1, 3] == 400)
solver.Add(x[2, 1] + x[2, 2] + x[2, 3] == 450)

# Demand constraints
# City 1: 290 <= x[1,1] + x[2,1] <= 320
solver.Add(x[1, 1] + x[2, 1] >= 290)
solver.Add(x[1, 1] + x[2, 1] <= 320)

# City 2: x[1,2] + x[2,2] = 250
solver.Add(x[1, 2] + x[2, 2] == 250)

# City 3: 270 <= x[1,3] + x[2,3] <= 350
solver.Add(x[1, 3] + x[2, 3] >= 270)
solver.Add(x[1, 3] + x[2, 3] <= 350)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")