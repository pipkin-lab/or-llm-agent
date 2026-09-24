from ortools.linear_solver import pywraplp

# Model Type: MILP (Integer Linear Programming) since x_s, y_s are integers
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
S = [1, 2, 3, 4, 5, 6]  # Shift start times
T = [1, 2, 3, 4, 5, 6]  # Demand periods

# Parameters
D = dict()
D[1] = 10
D[2] = 15
D[3] = 25
D[4] = 20
D[5] = 18
D[6] = 12

Cost_FT = 80  # Total cost per 8-hour shift for a full-time nurse
Cost_CT = 120  # Total cost per 8-hour shift for a contract nurse

# Decision Variables
x = dict()
y = dict()
for s in S:
    x[s] = solver.IntVar(0, solver.infinity(), 'x_' + str(s))
    y[s] = solver.IntVar(0, solver.infinity(), 'y_' + str(s))

# Objective Function: Minimize total labor cost
obj = 0
for s in S:
    obj += Cost_FT * x[s] + Cost_CT * y[s]
solver.Minimize(obj)

# Coverage Constraints
# Period 1 (02:00-06:00): Covered by Shift 6 (ending) and Shift 1 (starting)
solver.Add((x[6] + y[6]) + (x[1] + y[1]) >= D[1])
# Period 2 (06:00-10:00): Covered by Shift 1 (ending) and Shift 2 (starting)
solver.Add((x[1] + y[1]) + (x[2] + y[2]) >= D[2])
# Period 3 (10:00-14:00): Covered by Shift 2 (ending) and Shift 3 (starting)
solver.Add((x[2] + y[2]) + (x[3] + y[3]) >= D[3])
# Period 4 (14:00-18:00): Covered by Shift 3 (ending) and Shift 4 (starting)
solver.Add((x[3] + y[3]) + (x[4] + y[4]) >= D[4])
# Period 5 (18:00-22:00): Covered by Shift 4 (ending) and Shift 5 (starting)
solver.Add((x[4] + y[4]) + (x[5] + y[5]) >= D[5])
# Period 6 (22:00-02:00): Covered by Shift 5 (ending) and Shift 6 (starting)
solver.Add((x[5] + y[5]) + (x[6] + y[6]) >= D[6])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")