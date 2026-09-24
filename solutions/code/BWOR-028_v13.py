from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x_s for s = 1..6, non-negative integers
x = dict()
for s in range(1, 7):
    x[s] = solver.IntVar(0, INF, 'x_' + str(s))

# Demand parameters
D = dict()
D[1] = 10
D[2] = 15
D[3] = 25
D[4] = 20
D[5] = 18
D[6] = 12

# Objective: minimize total nurses
solver.Minimize(x[1] + x[2] + x[3] + x[4] + x[5] + x[6])

# Constraints
# Period 1: x_1 + x_6 >= 10
solver.Add(x[1] + x[6] >= D[1])
# Period 2: x_1 + x_2 >= 15
solver.Add(x[1] + x[2] >= D[2])
# Period 3: x_2 + x_3 >= 25
solver.Add(x[2] + x[3] >= D[3])
# Period 4: x_3 + x_4 >= 20
solver.Add(x[3] + x[4] >= D[4])
# Period 5: x_4 + x_5 >= 18
solver.Add(x[4] + x[5] >= D[5])
# Period 6: x_5 + x_6 >= 12
solver.Add(x[5] + x[6] >= D[6])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")