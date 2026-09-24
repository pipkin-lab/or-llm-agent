from ortools.linear_solver import pywraplp

# Initialize solver for MILP
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
heights = {
    1: 1.92,
    2: 1.90,
    3: 1.88,
    4: 1.86,
    5: 1.85,
    6: 1.83,
    7: 1.80,
    8: 1.78
}

players = [1, 2, 3, 4, 5, 6, 7, 8]

# Decision Variables: binary variables for each player
x = dict()
for i in players:
    x[i] = solver.BoolVar('x_' + str(i))

# Objective Function: Maximize sum of heights
obj = 0
for i in players:
    obj += heights[i] * x[i]

solver.Maximize(obj)

# Constraint 1: Team Size - Exactly 5 players
solver.Add(sum(x[i] for i in players) == 5)

# Constraint 2: Exactly One Center (Players 1 and 2)
solver.Add(x[1] + x[2] == 1)

# Constraint 3: At Least One Forward (Players 3, 4, 5)
solver.Add(x[3] + x[4] + x[5] >= 1)

# Constraint 4: Conditional Selection Logic
# The logic implies x1 = 0 and x4 = 0
# We enforce the direct result derived from the mutual exclusion and dependency
solver.Add(x[1] == 0)
solver.Add(x[4] == 0)

# Constraint 5: Mutual Exclusion of Player 2 and Player 8
solver.Add(x[2] + x[8] <= 1)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")