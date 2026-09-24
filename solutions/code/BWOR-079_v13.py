from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x_i for i in 1..5 (number of nurses on Shift i)
x = dict()
for i in range(1, 6):
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

# Coverage constraints
# Period 1 (6-10): Shift 1 + Shift 2 >= 18
solver.Add(x[1] + x[2] >= 18)
# Period 2 (10-14): Shift 2 + Shift 3 >= 20
solver.Add(x[2] + x[3] >= 20)
# Period 3 (14-18): Shift 3 + Shift 4 >= 19
solver.Add(x[3] + x[4] >= 19)
# Period 4 (18-22): Shift 4 + Shift 5 >= 17
solver.Add(x[4] + x[5] >= 17)
# Period 5 (22-6): Shift 5 + Shift 1 >= 12
solver.Add(x[5] + x[1] >= 12)

# Plan 1 structural constraints: all shifts have equal staffing
solver.Add(x[1] == x[2])
solver.Add(x[2] == x[3])
solver.Add(x[3] == x[4])
solver.Add(x[4] == x[5])

# Objective: Minimize total nurses Z = 7 * x[1]
solver.Minimize(7 * x[1])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")