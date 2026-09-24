from ortools.linear_solver import pywraplp

# Initialize the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define the index set for shift start times (1-indexed as per model)
shifts = [1, 2, 3, 4, 5, 6]

# Decision variables
# x[i]: number of full-time nurses for shift i
# y[i]: number of contract nurses for shift i
x = dict()
y = dict()

for i in shifts:
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))
    y[i] = solver.IntVar(0, solver.infinity(), 'y_' + str(i))

# Objective function: Minimize total cost
# Full-time cost per shift: 80
# Contract cost per shift: 120
objective = 0
for i in shifts:
    objective += 80 * x[i] + 120 * y[i]

solver.Minimize(objective)

# Constraints: Coverage for each 4-hour period
# Period 1 (2:00-6:00): Covered by shifts i=6 and i=1. Requirement: 10
solver.Add(x[6] + y[6] + x[1] + y[1] >= 10)

# Period 2 (6:00-10:00): Covered by shifts i=1 and i=2. Requirement: 15
solver.Add(x[1] + y[1] + x[2] + y[2] >= 15)

# Period 3 (10:00-14:00): Covered by shifts i=2 and i=3. Requirement: 25
solver.Add(x[2] + y[2] + x[3] + y[3] >= 25)

# Period 4 (14:00-18:00): Covered by shifts i=3 and i=4. Requirement: 20
solver.Add(x[3] + y[3] + x[4] + y[4] >= 20)

# Period 5 (18:00-22:00): Covered by shifts i=4 and i=5. Requirement: 18
solver.Add(x[4] + y[4] + x[5] + y[5] >= 18)

# Period 6 (22:00-2:00): Covered by shifts i=5 and i=6. Requirement: 12
solver.Add(x[5] + y[5] + x[6] + y[6] >= 12)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")