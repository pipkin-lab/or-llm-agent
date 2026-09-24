from ortools.linear_solver import pywraplp

# Define parameters
I = [0, 1, 2]  # Departments (0-indexed)
X = [0, 1, 2, 3]  # Possible units of Resource 1
Y = [0, 1, 2, 3]  # Possible units of Resource 2
R1 = 3  # Total available units of Resource 1
R2 = 3  # Total available units of Resource 2

# Profit matrices
profit = {}
# Department 1 (index 0)
profit[(0, 0, 0)] = 0
profit[(0, 0, 1)] = 1
profit[(0, 0, 2)] = 3
profit[(0, 0, 3)] = 6
profit[(0, 1, 0)] = 4
profit[(0, 1, 1)] = 5
profit[(0, 1, 2)] = 6
profit[(0, 1, 3)] = 7
profit[(0, 2, 0)] = 5
profit[(0, 2, 1)] = 6
profit[(0, 2, 2)] = 7
profit[(0, 2, 3)] = 8
profit[(0, 3, 0)] = 6
profit[(0, 3, 1)] = 7
profit[(0, 3, 2)] = 8
profit[(0, 3, 3)] = 9

# Department 2 (index 1)
profit[(1, 0, 0)] = 0
profit[(1, 0, 1)] = 2
profit[(1, 0, 2)] = 4
profit[(1, 0, 3)] = 6
profit[(1, 1, 0)] = 1
profit[(1, 1, 1)] = 4
profit[(1, 1, 2)] = 6
profit[(1, 1, 3)] = 7
profit[(1, 2, 0)] = 4
profit[(1, 2, 1)] = 6
profit[(1, 2, 2)] = 8
profit[(1, 2, 3)] = 9
profit[(1, 3, 0)] = 6
profit[(1, 3, 1)] = 8
profit[(1, 3, 2)] = 10
profit[(1, 3, 3)] = 11

# Department 3 (index 2)
profit[(2, 0, 0)] = 0
profit[(2, 0, 1)] = 3
profit[(2, 0, 2)] = 5
profit[(2, 0, 3)] = 8
profit[(2, 1, 0)] = 2
profit[(2, 1, 1)] = 5
profit[(2, 1, 2)] = 7
profit[(2, 1, 3)] = 9
profit[(2, 2, 0)] = 4
profit[(2, 2, 1)] = 7
profit[(2, 2, 2)] = 9
profit[(2, 2, 3)] = 11
profit[(2, 3, 0)] = 6
profit[(2, 3, 1)] = 9
profit[(2, 3, 2)] = 11
profit[(2, 3, 3)] = 13

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Create binary decision variables z[i, x, y]
z = {}
for i in I:
    for x in X:
        for y in Y:
            z[i, x, y] = solver.BoolVar(f'z_{i}_{x}_{y}')

# Objective function: Maximize total profit
objective = 0
for i in I:
    for x in X:
        for y in Y:
            objective += profit[(i, x, y)] * z[i, x, y]
solver.Maximize(objective)

# Constraint 1: Single allocation state per department
for i in I:
    constraint = solver.Constraint(1, 1)
    for x in X:
        for y in Y:
            constraint.SetCoefficient(z[i, x, y], 1)
    solver.Add(constraint)

# Constraint 2: Total Resource 1 availability
res1_constraint = solver.Constraint(0, R1)
for i in I:
    for x in X:
        for y in Y:
            res1_constraint.SetCoefficient(z[i, x, y], x)
solver.Add(res1_constraint)

# Constraint 3: Total Resource 2 availability
res2_constraint = solver.Constraint(0, R2)
for i in I:
    for x in X:
        for y in Y:
            res2_constraint.SetCoefficient(z[i, x, y], y)
solver.Add(res2_constraint)

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")