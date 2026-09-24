from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
inf = solver.infinity()

# Decision variables x[i][j] for i in {1,2}, j in {1,2,3}
x = dict()
for i in range(1, 3):
    for j in range(1, 4):
        x[i, j] = solver.NumVar(0, inf, 'x_%d_%d' % (i, j))

# Supply constraints: each station uses up all available electricity
solver.Add(x[1, 1] + x[1, 2] + x[1, 3] == 400)
solver.Add(x[2, 1] + x[2, 2] + x[2, 3] == 450)

# Demand constraints
# City 1: 290 <= x11 + x21 <= 320
solver.Add(x[1, 1] + x[2, 1] >= 290)
solver.Add(x[1, 1] + x[2, 1] <= 320)

# City 2: x12 + x22 = 250
solver.Add(x[1, 2] + x[2, 2] == 250)

# City 3: 270 <= x13 + x23 <= 350
solver.Add(x[1, 3] + x[2, 3] >= 270)
solver.Add(x[1, 3] + x[2, 3] <= 350)

# Objective: minimize total cost
objective = 15 * x[1, 1] + 18 * x[1, 2] + 22 * x[1, 3] \
          + 21 * x[2, 1] + 25 * x[2, 2] + 16 * x[2, 3]
solver.Minimize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")