from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
P = [1, 2, 3, 4, 5, 6, 7, 8]
PC = [1, 2]
PF = [3, 4, 5]
PG = [6, 7, 8]

# Parameters
h = dict()
h[1] = 1.92
h[2] = 1.90
h[3] = 1.88
h[4] = 1.86
h[5] = 1.85
h[6] = 1.83
h[7] = 1.80
h[8] = 1.78

N = 5

# Decision variables
x = dict()
for i in P:
    x[i] = solver.BoolVar('x_' + str(i))

# Objective: Maximize total height
obj = sum(h[i] * x[i] for i in P)
solver.Maximize(obj)

# Constraint 1: Exactly 5 players
solver.Add(sum(x[i] for i in P) == N)

# Constraint 2: Exactly one center (players 1 and 2)
solver.Add(x[1] + x[2] == 1)

# Constraint 3: At least one forward (players 3, 4, 5)
solver.Add(x[3] + x[4] + x[5] >= 1)

# Constraint 4: Logical implications
# x1 <= x6
solver.Add(x[1] - x[6] <= 0)
# x4 <= x6
solver.Add(x[4] - x[6] <= 0)
# x1 + x6 <= 1
solver.Add(x[1] + x[6] <= 1)
# x4 + x6 <= 1
solver.Add(x[4] + x[6] <= 1)

# Constraint 5: Player 2 and Player 8 mutual exclusion
solver.Add(x[2] + x[8] <= 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")