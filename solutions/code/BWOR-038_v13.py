from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: x[m][p] = units of product p processed on machine m
# Only define variables for allowed (machine, product) pairs

# Stage A variables
xA1_I = solver.NumVar(0, INF, 'xA1_I')
xA1_II = solver.NumVar(0, INF, 'xA1_II')

xA2_I = solver.NumVar(0, INF, 'xA2_I')
xA2_II = solver.NumVar(0, INF, 'xA2_II')
xA2_III = solver.NumVar(0, INF, 'xA2_III')

# Stage B variables
xB1_I = solver.NumVar(0, INF, 'xB1_I')
xB1_II = solver.NumVar(0, INF, 'xB1_II')

xB2_I = solver.NumVar(0, INF, 'xB2_I')
xB2_III = solver.NumVar(0, INF, 'xB2_III')

xB3_I = solver.NumVar(0, INF, 'xB3_I')

# Objective: Maximize Z
# Stage A coefficients: (s_p - r_p) - t_{m,p} * c_m
# Stage B coefficients: -t_{m,p} * c_m

# Product I: s-r = 1.25 - 0.25 = 1.00
# A1: 1.00 - 5*0.05 = 0.75
# A2: 1.00 - 7*0.03 = 0.79
# B1: -6*0.06 = -0.36
# B2: -4*0.11 = -0.44
# B3: -7*0.05 = -0.35

# Product II: s-r = 2.00 - 0.35 = 1.65
# A1: 1.65 - 10*0.05 = 1.15
# A2: 1.65 - 9*0.03 = 1.38
# B1: -8*0.06 = -0.48

# Product III: s-r = 2.80 - 0.50 = 2.30
# A2: 2.30 - 12*0.03 = 1.94
# B2: -11*0.11 = -1.21

obj = (0.75 * xA1_I + 0.79 * xA2_I + 1.15 * xA1_II + 1.38 * xA2_II + 1.94 * xA2_III
       - 0.36 * xB1_I - 0.44 * xB2_I - 0.35 * xB3_I - 0.48 * xB1_II - 1.21 * xB2_III)
solver.Maximize(obj)

# Machine Capacity Constraints
# A1: 5*x_A1,I + 10*x_A1,II <= 6000
solver.Add(5 * xA1_I + 10 * xA1_II <= 6000)

# A2: 7*x_A2,I + 9*x_A2,II + 12*x_A2,III <= 10000
solver.Add(7 * xA2_I + 9 * xA2_II + 12 * xA2_III <= 10000)

# B1: 6*x_B1,I + 8*x_B1,II <= 4000
solver.Add(6 * xB1_I + 8 * xB1_II <= 4000)

# B2: 4*x_B2,I + 11*x_B2,III <= 7000
solver.Add(4 * xB2_I + 11 * xB2_III <= 7000)

# B3: 7*x_B3,I <= 4000
solver.Add(7 * xB3_I <= 4000)

# Flow Balance Constraints
# Product I: x_A1,I + x_A2,I = x_B1,I + x_B2,I + x_B3,I
solver.Add(xA1_I + xA2_I == xB1_I + xB2_I + xB3_I)

# Product II: x_A1,II + x_A2,II = x_B1,II
solver.Add(xA1_II + xA2_II == xB1_II)

# Product III: x_A2,III = x_B2,III
solver.Add(xA2_III == xB2_III)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")