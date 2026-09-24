from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
h = [1.92, 1.90, 1.88, 1.86, 1.85, 1.83, 1.80, 1.78]
N_PLAYERS = 8

# Decision variables
x = dict()
for i in range(N_PLAYERS):
    x[i] = solver.BoolVar('x_' + str(i))

# Objective: Maximize total height
obj_terms = [h[i] * x[i] for i in range(N_PLAYERS)]
solver.Maximize(sum(obj_terms))

# Constraint 1: Exactly 5 players selected
solver.Add(sum(x[i] for i in range(N_PLAYERS)) == 5)

# Constraint 2: Exactly one center (players 0 and 1, i.e., 1 and 2)
solver.Add(x[0] + x[1] == 1)

# Constraint 3: At least one forward (players 2, 3, 4, i.e., 3, 4, 5)
solver.Add(x[2] + x[3] + x[4] >= 1)

# Constraint 4: x1 <= x6 (player 1 implies player 6)
# Note: player indices in code are 0-based, so player 1 is x[0], player 6 is x[5]
solver.Add(x[0] <= x[5])

# Constraint 5: x4 <= x6 (player 4 implies player 6)
# Player 4 is x[3], player 6 is x[5]
solver.Add(x[3] <= x[5])

# Constraint 6: x1 + x6 <= 1
solver.Add(x[0] + x[5] <= 1)

# Constraint 7: x4 + x6 <= 1
solver.Add(x[3] + x[5] <= 1)

# Constraint 8: x2 + x8 <= 1 (player 2 and player 8 mutually exclusive)
# Player 2 is x[1], player 8 is x[7]
solver.Add(x[1] + x[7] <= 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")