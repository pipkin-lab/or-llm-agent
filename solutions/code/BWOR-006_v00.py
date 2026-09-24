from ortools.linear_solver import pywraplp

# Initialize LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: Stage A
a11 = solver.NumVar(0, INF, 'a11')  # Product I on A1
a12 = solver.NumVar(0, INF, 'a12')  # Product II on A1
a21 = solver.NumVar(0, INF, 'a21')  # Product I on A2
a22 = solver.NumVar(0, INF, 'a22')  # Product II on A2
a23 = solver.NumVar(0, INF, 'a23')  # Product III on A2

# Decision variables: Stage B
b11 = solver.NumVar(0, INF, 'b11')  # Product I on B1
b21 = solver.NumVar(0, INF, 'b21')  # Product II on B1
b12 = solver.NumVar(0, INF, 'b12')  # Product I on B2
b32 = solver.NumVar(0, INF, 'b32')  # Product III on B2
b13 = solver.NumVar(0, INF, 'b13')  # Product I on B3

# Auxiliary variables: total quantity per product
Q_I = solver.NumVar(0, INF, 'Q_I')
Q_II = solver.NumVar(0, INF, 'Q_II')
Q_III = solver.NumVar(0, INF, 'Q_III')

# Flow balance constraints
solver.Add(Q_I == a11 + a21)
solver.Add(Q_I == b11 + b12 + b13)
solver.Add(Q_II == a12 + a22)
solver.Add(Q_II == b21)
solver.Add(Q_III == a23)
solver.Add(Q_III == b32)

# Machine capacity constraints
# A1: 5*a11 + 10*a12 <= 6000
solver.Add(5 * a11 + 10 * a12 <= 6000)
# A2: 7*a21 + 9*a22 + 12*a23 <= 10000
solver.Add(7 * a21 + 9 * a22 + 12 * a23 <= 10000)
# B1: 6*b11 + 8*b21 <= 4000
solver.Add(6 * b11 + 8 * b21 <= 4000)
# B2: 4*b12 + 11*b32 <= 7000
solver.Add(4 * b12 + 11 * b32 <= 7000)
# B3: 7*b13 <= 4000
solver.Add(7 * b13 <= 4000)

# Objective function: Maximize Z = 1.00*Q_I + 1.65*Q_II + 2.30*Q_III
# - (0.25*a11 + 0.50*a12) - (0.21*a21 + 0.27*a22 + 0.36*a23)
# - (0.36*b11 + 0.48*b21) - (0.44*b12 + 1.21*b32) - (0.35*b13)
obj = (1.00 * Q_I + 1.65 * Q_II + 2.30 * Q_III
       - 0.25 * a11 - 0.50 * a12
       - 0.21 * a21 - 0.27 * a22 - 0.36 * a23
       - 0.36 * b11 - 0.48 * b21
       - 0.44 * b12 - 1.21 * b32
       - 0.35 * b13)

solver.Maximize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")