from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
# Required number of nurses for each time period
R = [18, 20, 19, 17, 12]

# Decision Variables
# S[k] represents the number of nurses starting their 5-day work week on day k (0-indexed for days 0-6)
S = dict()
for k in range(7):
    S[k] = solver.IntVar(0, solver.infinity(), 'S_' + str(k))

# Objective Function
# Minimize total number of nurses
obj = sum(S[k] for k in range(7))
solver.Minimize(obj)

# Constraints
# Based on the derived mapping of start days to shifts on each day of the week.
# Days are 0-6 (corresponding to Day 1-7 in the problem description)
# Periods are 0-4 (corresponding to Period 1-5)

# Day 0 (Day 1):
# P0: S_0 + S_6 >= 18
# P1: S_6 + S_5 >= 20
# P2: S_5 + S_4 >= 19
# P3: S_4 + S_3 >= 17
# P4: S_3 + S_0 >= 12
solver.Add(S[0] + S[6] >= R[0])
solver.Add(S[6] + S[5] >= R[1])
solver.Add(S[5] + S[4] >= R[2])
solver.Add(S[4] + S[3] >= R[3])
solver.Add(S[3] + S[0] >= R[4])

# Day 1 (Day 2):
# P0: S_1 + S_0 >= 18
# P1: S_0 + S_6 >= 20
# P2: S_6 + S_5 >= 19
# P3: S_5 + S_4 >= 17
# P4: S_4 + S_1 >= 12
solver.Add(S[1] + S[0] >= R[0])
solver.Add(S[0] + S[6] >= R[1])
solver.Add(S[6] + S[5] >= R[2])
solver.Add(S[5] + S[4] >= R[3])
solver.Add(S[4] + S[1] >= R[4])

# Day 2 (Day 3):
# P0: S_2 + S_1 >= 18
# P1: S_1 + S_0 >= 20
# P2: S_0 + S_6 >= 19
# P3: S_6 + S_5 >= 17
# P4: S_5 + S_2 >= 12
solver.Add(S[2] + S[1] >= R[0])
solver.Add(S[1] + S[0] >= R[1])
solver.Add(S[0] + S[6] >= R[2])
solver.Add(S[6] + S[5] >= R[3])
solver.Add(S[5] + S[2] >= R[4])

# Day 3 (Day 4):
# P0: S_3 + S_2 >= 18
# P1: S_2 + S_1 >= 20
# P2: S_1 + S_0 >= 19
# P3: S_0 + S_6 >= 17
# P4: S_6 + S_3 >= 12
solver.Add(S[3] + S[2] >= R[0])
solver.Add(S[2] + S[1] >= R[1])
solver.Add(S[1] + S[0] >= R[2])
solver.Add(S[0] + S[6] >= R[3])
solver.Add(S[6] + S[3] >= R[4])

# Day 4 (Day 5):
# P0: S_4 + S_3 >= 18
# P1: S_3 + S_2 >= 20
# P2: S_2 + S_1 >= 19
# P3: S_1 + S_0 >= 17
# P4: S_0 + S_4 >= 12
solver.Add(S[4] + S[3] >= R[0])
solver.Add(S[3] + S[2] >= R[1])
solver.Add(S[2] + S[1] >= R[2])
solver.Add(S[1] + S[0] >= R[3])
solver.Add(S[0] + S[4] >= R[4])

# Day 5 (Day 6):
# P0: S_5 + S_4 >= 18
# P1: S_4 + S_3 >= 20
# P2: S_3 + S_2 >= 19
# P3: S_2 + S_1 >= 17
# P4: S_1 + S_5 >= 12
solver.Add(S[5] + S[4] >= R[0])
solver.Add(S[4] + S[3] >= R[1])
solver.Add(S[3] + S[2] >= R[2])
solver.Add(S[2] + S[1] >= R[3])
solver.Add(S[1] + S[5] >= R[4])

# Day 6 (Day 7):
# P0: S_6 + S_5 >= 18
# P1: S_5 + S_4 >= 20
# P2: S_4 + S_3 >= 19
# P3: S_3 + S_2 >= 17
# P4: S_2 + S_6 >= 12
solver.Add(S[6] + S[5] >= R[0])
solver.Add(S[5] + S[4] >= R[1])
solver.Add(S[4] + S[3] >= R[2])
solver.Add(S[3] + S[2] >= R[3])
solver.Add(S[2] + S[6] >= R[4])

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")