from ortools.linear_solver import pywraplp

# Initialize the solver (MILP since variables are binary)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Define the set of players
I = [1, 2, 3, 4, 5, 6, 7, 8]
R_C = [1, 2]
R_F = [3, 4, 5]
R_G = [6, 7, 8]

# Parameters: Heights
h = {
    1: 1.92,
    2: 1.90,
    3: 1.88,
    4: 1.86,
    5: 1.85,
    6: 1.83,
    7: 1.80,
    8: 1.78
}

# Decision Variables: x[i] is 1 if player i is selected, 0 otherwise
x = dict()
for i in I:
    x[i] = solver.BoolVar('x_' + str(i))

# Objective Function: Maximize total height
obj_terms = []
for i in I:
    obj_terms.append(h[i] * x[i])
solver.Maximize(sum(obj_terms))

# Constraints

# 1. Lineup Size Constraint: Exactly 5 players
solver.Add(sum(x[i] for i in I) == 5)

# 2. Positional Requirements
# Exactly one Center
solver.Add(sum(x[i] for i in R_C) == 1)

# At least one Forward
solver.Add(sum(x[i] for i in R_F) >= 1)

# 3. Logical Constraints (Player 1, Player 4, Player 6)
# Constraint A: If Player 1 is selected, Player 6 must be selected (x1 <= x6)
solver.Add(x[1] - x[6] <= 0)

# Constraint B: If Player 4 is selected, Player 6 must be selected (x4 <= x6)
solver.Add(x[4] - x[6] <= 0)

# Constraint C: If Player 6 is selected, Player 1 cannot be selected (x1 + x6 <= 1)
solver.Add(x[1] + x[6] <= 1)

# Constraint D: If Player 6 is selected, Player 4 cannot be selected (x4 + x6 <= 1)
solver.Add(x[4] + x[6] <= 1)

# 4. Player 2 and Player 8 Constraint: Cannot both be selected
solver.Add(x[2] + x[8] <= 1)

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")