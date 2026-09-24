from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
x_I_A1 = solver.NumVar(0, INF, 'x_I_A1')
x_I_A2 = solver.NumVar(0, INF, 'x_I_A2')
x_II_A1 = solver.NumVar(0, INF, 'x_II_A1')
x_II_A2 = solver.NumVar(0, INF, 'x_II_A2')
x_III_A2 = solver.NumVar(0, INF, 'x_III_A2')

x_I_B1 = solver.NumVar(0, INF, 'x_I_B1')
x_I_B2 = solver.NumVar(0, INF, 'x_I_B2')
x_I_B3 = solver.NumVar(0, INF, 'x_I_B3')
x_II_B1 = solver.NumVar(0, INF, 'x_II_B1')
x_III_B2 = solver.NumVar(0, INF, 'x_III_B2')

Q_I = solver.NumVar(0, INF, 'Q_I')
Q_II = solver.NumVar(0, INF, 'Q_II')
Q_III = solver.NumVar(0, INF, 'Q_III')

# Flow balance constraints
solver.Add(x_I_A1 + x_I_A2 == Q_I)
solver.Add(x_I_B1 + x_I_B2 + x_I_B3 == Q_I)
solver.Add(x_II_A1 + x_II_A2 == Q_II)
solver.Add(x_II_B1 == Q_II)
solver.Add(x_III_A2 == Q_III)
solver.Add(x_III_B2 == Q_III)

# Machine capacity constraints
solver.Add(5 * x_I_A1 + 10 * x_II_A1 <= 6000)
solver.Add(7 * x_I_A2 + 9 * x_II_A2 + 12 * x_III_A2 <= 10000)
solver.Add(6 * x_I_B1 + 8 * x_II_B1 <= 4000)
solver.Add(4 * x_I_B2 + 11 * x_III_B2 <= 7000)
solver.Add(7 * x_I_B3 <= 4000)

# Objective function
objective = (1.00 * Q_I - 0.25 * x_I_A1 - 0.21 * x_I_A2 - 0.36 * x_I_B1
             - 0.44 * x_I_B2 - 0.35 * x_I_B3
             + 1.65 * Q_II - 0.50 * x_II_A1 - 0.27 * x_II_A2 - 0.48 * x_II_B1
             + 2.30 * Q_III - 0.36 * x_III_A2 - 1.21 * x_III_B2)

solver.Maximize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")