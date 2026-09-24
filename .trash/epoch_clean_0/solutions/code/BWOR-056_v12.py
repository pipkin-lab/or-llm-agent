from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x_c for c in {1, 2, 3, 4, 5, 6, 7}
x = dict()
for c in range(1, 8):
    x[c] = solver.BoolVar('x_' + str(c))

# Objective: minimize total number of courses
objective = x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7]
solver.Minimize(objective)

# Category constraints (equality)
# Math: x1 + x2 + x3 + x4 + x7 = 2
solver.Add(x[1] + x[2] + x[3] + x[4] + x[7] == 2)

# OR: x2 + x4 + x5 + x7 = 2
solver.Add(x[2] + x[4] + x[5] + x[7] == 2)

# CS: x3 + x5 + x6 = 2
solver.Add(x[3] + x[5] + x[6] == 2)

# Prerequisite constraints
# x5 <= x6
solver.Add(x[5] <= x[6])
# x3 <= x6
solver.Add(x[3] <= x[6])
# x4 <= x1
solver.Add(x[4] <= x[1])
# x7 <= x4
solver.Add(x[7] <= x[4])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")