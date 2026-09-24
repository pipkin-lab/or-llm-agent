from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision Variables (Stage A)
x_I_A1 = solver.NumVar(0, INF, 'x_I_A1')
x_I_A2 = solver.NumVar(0, INF, 'x_I_A2')
x_II_A1 = solver.NumVar(0, INF, 'x_II_A1')
x_II_A2 = solver.NumVar(0, INF, 'x_II_A2')
x_III_A2 = solver.NumVar(0, INF, 'x_III_A2')

# Decision Variables (Stage B)
y_I_B1 = solver.NumVar(0, INF, 'y_I_B1')
y_I_B2 = solver.NumVar(0, INF, 'y_I_B2')
y_I_B3 = solver.NumVar(0, INF, 'y_I_B3')
y_II_B1 = solver.NumVar(0, INF, 'y_II_B1')
y_III_B2 = solver.NumVar(0, INF, 'y_III_B2')

# Objective Function
# Maximize Z = 0.75*x_I_A1 + 0.79*x_I_A2 + 1.15*x_II_A1 + 1.38*x_II_A2 + 1.94*x_III_A2
#              - 0.36*y_I_B1 - 0.44*y_I_B2 - 0.35*y_I_B3 - 0.48*y_II_B1 - 1.21*y_III_B2
objective = (0.75 * x_I_A1 + 0.79 * x_I_A2 + 1.15 * x_II_A1 + 1.38 * x_II_A2 + 1.94 * x_III_A2
             - 0.36 * y_I_B1 - 0.44 * y_I_B2 - 0.35 * y_I_B3 - 0.48 * y_II_B1 - 1.21 * y_III_B2)
solver.Maximize(objective)

# Constraint 1: Machine A1 Capacity
solver.Add(5 * x_I_A1 + 10 * x_II_A1 <= 6000)

# Constraint 2: Machine A2 Capacity
solver.Add(7 * x_I_A2 + 9 * x_II_A2 + 12 * x_III_A2 <= 10000)

# Constraint 3: Machine B1 Capacity
solver.Add(6 * y_I_B1 + 8 * y_II_B1 <= 4000)

# Constraint 4: Machine B2 Capacity
solver.Add(4 * y_I_B2 + 11 * y_III_B2 <= 7000)

# Constraint 5: Machine B3 Capacity
solver.Add(7 * y_I_B3 <= 4000)

# Constraint 6: Flow Balance Product I
solver.Add(x_I_A1 + x_I_A2 == y_I_B1 + y_I_B2 + y_I_B3)

# Constraint 7: Flow Balance Product II
solver.Add(x_II_A1 + x_II_A2 == y_II_B1)

# Constraint 8: Flow Balance Product III
solver.Add(x_III_A2 == y_III_B2)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")