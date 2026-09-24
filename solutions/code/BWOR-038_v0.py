from ortools.linear_solver import pywraplp

# Define the solver (LP)
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
# Stage A variables
xA1_1 = solver.NumVar(0, INF, 'xA1_1')  # Product I on A1
xA1_2 = solver.NumVar(0, INF, 'xA1_2')  # Product II on A1
xA2_1 = solver.NumVar(0, INF, 'xA2_1')  # Product I on A2
xA2_2 = solver.NumVar(0, INF, 'xA2_2')  # Product II on A2
xA2_3 = solver.NumVar(0, INF, 'xA2_3')  # Product III on A2

# Stage B variables
xB1_1 = solver.NumVar(0, INF, 'xB1_1')  # Product I on B1
xB1_2 = solver.NumVar(0, INF, 'xB1_2')  # Product II on B1
xB2_1 = solver.NumVar(0, INF, 'xB2_1')  # Product I on B2
xB2_3 = solver.NumVar(0, INF, 'xB2_3')  # Product III on B2
xB3_1 = solver.NumVar(0, INF, 'xB3_1')  # Product I on B3

# Total production variables (Q_j)
Q1 = solver.NumVar(0, INF, 'Q1')
Q2 = solver.NumVar(0, INF, 'Q2')
Q3 = solver.NumVar(0, INF, 'Q3')

# Q_j definitions from Stage A
solver.Add(Q1 == xA1_1 + xA2_1)
solver.Add(Q2 == xA1_2 + xA2_2)
solver.Add(Q3 == xA2_3)

# Flow balance constraints
# Product I: Stage A total = Stage B total
solver.Add(xA1_1 + xA2_1 == xB1_1 + xB2_1 + xB3_1)
# Product II: Stage A total = Stage B total (only B1)
solver.Add(xA1_2 + xA2_2 == xB1_2)
# Product III: Stage A total = Stage B total (only B2)
solver.Add(xA2_3 == xB2_3)

# Stage A capacity constraints (minutes)
# A1: 6000 hours * 60 = 360000 minutes
solver.Add(5 * xA1_1 + 10 * xA1_2 <= 360000)
# A2: 10000 hours * 60 = 600000 minutes
solver.Add(7 * xA2_1 + 9 * xA2_2 + 12 * xA2_3 <= 600000)

# Stage B capacity constraints (minutes)
# B1: 4000 hours * 60 = 240000 minutes
solver.Add(6 * xB1_1 + 8 * xB1_2 <= 240000)
# B2: 7000 hours * 60 = 420000 minutes
solver.Add(4 * xB2_1 + 11 * xB2_3 <= 420000)
# B3: 4000 hours * 60 = 240000 minutes
solver.Add(7 * xB3_1 <= 240000)

# Objective function: Maximize profit
# Z = 1.00*Q1 + 1.65*Q2 + 2.30*Q3 - [processing costs]
# Processing costs:
#   0.25*xA1_1 + 0.50*xA1_2 + 0.21*xA2_1 + 0.27*xA2_2 + 0.36*xA2_3
# + 0.36*xB1_1 + 0.48*xB1_2 + 0.44*xB2_1 + 1.21*xB2_3 + 0.35*xB3_1

obj = (1.00 * Q1 + 1.65 * Q2 + 2.30 * Q3
       - (0.25 * xA1_1 + 0.50 * xA1_2 + 0.21 * xA2_1 + 0.27 * xA2_2 + 0.36 * xA2_3)
       - (0.36 * xB1_1 + 0.48 * xB1_2 + 0.44 * xB2_1 + 1.21 * xB2_3 + 0.35 * xB3_1))

solver.Maximize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")