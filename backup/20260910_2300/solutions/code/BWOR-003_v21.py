from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameters
D_2003 = 100
D_2004 = 150
D_2005 = 120
D_2006 = 110

r_bank = 1.04
R_A = 1.40
U_A = 60
R_B = 1.25
U_B = 90
R_C = 1.30
U_C = 50

# Decision variables
X0 = solver.NumVar(0, INF, 'X0')
xA = solver.NumVar(0, U_A, 'xA')
xB = solver.NumVar(0, U_B, 'xB')
xC = solver.NumVar(0, U_C, 'xC')
b2003 = solver.NumVar(0, INF, 'b2003')
b2004 = solver.NumVar(0, INF, 'b2004')
b2005 = solver.NumVar(0, INF, 'b2005')
b2006 = solver.NumVar(0, INF, 'b2006')

# Objective: Minimize X0
solver.Minimize(X0)

# Constraint 1: Year 2003 Cash Flow
# X0 - xA - xB - b2003 = D_2003
solver.Add(X0 - xA - xB - b2003 == D_2003)

# Constraint 2: Year 2004 Cash Flow
# 1.04 * b2003 - xC - b2004 = D_2004
solver.Add(r_bank * b2003 - xC - b2004 == D_2004)

# Constraint 3: Year 2005 Cash Flow
# 1.04 * b2004 + 1.25 * xB - b2005 = D_2005
solver.Add(r_bank * b2004 + R_B * xB - b2005 == D_2005)

# Constraint 4: Year 2006 Cash Flow
# 1.04 * b2005 + 1.40 * xA + 1.30 * xC - b2006 = D_2006
solver.Add(r_bank * b2005 + R_A * xA + R_C * xC - b2006 == D_2006)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")