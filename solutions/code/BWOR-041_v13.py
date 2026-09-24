from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
# x[(i, j)] for i in {A, B, C}, j in {X, Y, Z}
# x[(A, Z)] is fixed to 0, so we do not create it
I = ['A', 'B', 'C']
J = ['X', 'Y', 'Z']

x = dict()
for i in I:
    for j in J:
        if i == 'A' and j == 'Z':
            continue
        x[(i, j)] = solver.NumVar(0, 1500, 'x_' + i + '_' + j)

# x[A, Z] is implicitly 0 (not created)

# Supply constraints
# A: x[A,X] + x[A,Y] = 1000
solver.Add(x[('A', 'X')] + x[('A', 'Y')] == 1000)
# B: x[B,X] + x[B,Y] + x[B,Z] = 2000
solver.Add(x[('B', 'X')] + x[('B', 'Y')] + x[('B', 'Z')] == 2000)
# C: x[C,X] + x[C,Y] + x[C,Z] = 2000
solver.Add(x[('C', 'X')] + x[('C', 'Y')] + x[('C', 'Z')] == 2000)

# Demand/capacity constraints are already handled by variable upper bounds of 1500
# But let's add them explicitly for clarity (they are redundant with bounds but safe)
# Actually, since we set ub=1500, we don't need separate constraints.

# Specific business rules
# Store Z requires at least 1,000 units of Toy C
solver.Add(x[('C', 'Z')] >= 1000)
# Store Z refuses to accept Toy A: already handled by not creating x[A,Z]

# Objective function
obj = (5 * x[('A', 'X')] + 4 * x[('A', 'Y')]
       + 16 * x[('B', 'X')] + 8 * x[('B', 'Y')] + 6 * x[('B', 'Z')]
       + 12 * x[('C', 'X')] + 10 * x[('C', 'Y')] + 11 * x[('C', 'Z')])

solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")