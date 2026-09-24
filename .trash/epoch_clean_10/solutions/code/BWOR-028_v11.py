from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
num_shifts = 6
num_periods = 6

R = [10, 15, 25, 20, 18, 12]  # Requirements for periods 1 to 6 (0-indexed: 0 to 5)

# Coverage matrix a[t][s]: 1 if shift s covers period t
# Shifts are 0-indexed in code (0 to 5), Periods are 0-indexed (0 to 5)
# Based on the problem description:
# Shift 0 (02:00): covers Period 0 (02-06) and Period 1 (06-10)
# Shift 1 (06:00): covers Period 1 (06-10) and Period 2 (10-14)
# Shift 2 (10:00): covers Period 2 (10-14) and Period 3 (14-18)
# Shift 3 (14:00): covers Period 3 (14-18) and Period 4 (18-22)
# Shift 4 (18:00): covers Period 4 (18-22) and Period 5 (22-02)
# Shift 5 (22:00): covers Period 5 (22-02) and Period 0 (02-06)

a = [
    [1, 0, 0, 0, 0, 1],  # Period 0
    [1, 1, 0, 0, 0, 0],  # Period 1
    [0, 1, 1, 0, 0, 0],  # Period 2
    [0, 0, 1, 1, 0, 0],  # Period 3
    [0, 0, 0, 1, 1, 0],  # Period 4
    [0, 0, 0, 0, 1, 1]   # Period 5
]

# Decision Variables
# x[s] is the number of nurses starting shift s
x = dict()
for s in range(num_shifts):
    x[s] = solver.IntVar(0, solver.infinity(), 'x_' + str(s))

# Objective Function
# Minimize total number of nurses
obj = sum(x[s] for s in range(num_shifts))
solver.Minimize(obj)

# Constraints
# For each period t, sum of nurses covering that period >= R[t]
for t in range(num_periods):
    constraint = sum(a[t][s] * x[s] for s in range(num_shifts))
    solver.Add(constraint >= R[t])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")