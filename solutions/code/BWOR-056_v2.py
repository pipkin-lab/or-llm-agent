from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Course indices
# 1: Calculus (CAL)
# 2: Operations Research (OR)
# 3: Data Structures (DS)
# 4: Managerial Statistics (STAT)
# 5: Computer Simulation (SIM)
# 6: Computer Programming (CP)
# 7: Forecasting (FC)

# Decision Variables
x = dict()
for i in range(1, 8):
    x[i] = solver.BoolVar('x_' + str(i))

# Objective: Minimize total number of courses
obj = sum(x[i] for i in range(1, 8))
solver.Minimize(obj)

# Category Requirements
# Math: CAL(1), OR(2), DS(3), STAT(4), FC(7) >= 2
solver.Add(x[1] + x[2] + x[3] + x[4] + x[7] >= 2)

# OR: OR(2), STAT(4), SIM(5), FC(7) >= 2
solver.Add(x[2] + x[4] + x[5] + x[7] >= 2)

# CS: DS(3), SIM(5), CP(6) >= 2
solver.Add(x[3] + x[5] + x[6] >= 2)

# Prerequisite Constraints
# SIM(5) requires CP(6)
solver.Add(x[5] <= x[6])

# DS(3) requires CP(6)
solver.Add(x[3] <= x[6])

# STAT(4) requires CAL(1)
solver.Add(x[4] <= x[1])

# FC(7) requires STAT(4)
solver.Add(x[7] <= x[4])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")