from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters: net cost c[i][j] for buying at start of year i and selling at end of year j
c = dict()
c[1, 1] = 0.8
c[1, 2] = 2.0
c[1, 3] = 3.8
c[1, 4] = 6.0
c[2, 2] = 0.9
c[2, 3] = 2.1
c[2, 4] = 3.9
c[3, 3] = 1.1
c[3, 4] = 2.3
c[4, 4] = 1.4

# Decision variables: x[i, j] is binary, 1 if machine bought at start of year i and sold at end of year j
x = dict()
for i in range(1, 5):
    for j in range(i, 5):
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: minimize total cost
obj = 0
for i in range(1, 5):
    for j in range(i, 5):
        obj += c[i, j] * x[i, j]
solver.Minimize(obj)

# Constraints
# 1. Start Constraint (Year 1)
solver.Add(x[1, 1] + x[1, 2] + x[1, 3] + x[1, 4] == 1)

# 2. Transition Constraint (Year 2)
solver.Add(x[2, 2] + x[2, 3] + x[2, 4] == x[1, 1])

# 3. Transition Constraint (Year 3)
solver.Add(x[3, 3] + x[3, 4] == x[1, 2] + x[2, 2])

# 4. Transition Constraint (Year 4)
solver.Add(x[4, 4] == x[1, 3] + x[2, 3] + x[3, 3])

# 5. End Constraint (Year 4)
solver.Add(x[1, 4] + x[2, 4] + x[3, 4] + x[4, 4] == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")