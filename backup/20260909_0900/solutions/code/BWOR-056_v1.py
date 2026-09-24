from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Sets and parameters
# Courses: c1 to c7
# c1: Calculus, c2: Operations Research, c3: Data Structures, c4: Managerial Statistics
# c5: Computer Simulation, c6: Computer Programming, c7: Forecasting

# Decision variables: x_i = 1 if course i is selected
x = dict()
for i in range(1, 8):
    x[i] = solver.BoolVar('x_' + str(i))

# Category requirements
# Math (k=1): c1, c2, c3, c4, c7 -> need >= 2
solver.Add(x[1] + x[2] + x[3] + x[4] + x[7] >= 2)

# OR (k=2): c2, c4, c5, c7 -> need >= 2
solver.Add(x[2] + x[4] + x[5] + x[7] >= 2)

# CS (k=3): c3, c5, c6 -> need >= 2
solver.Add(x[3] + x[5] + x[6] >= 2)

# Prerequisite constraints
# P = {(6, 3), (6, 5), (1, 4), (4, 7)}
# (i, j) means if j is taken, i must be taken -> x_j <= x_i

# To take c3 (Data Structures), must take c6 (Comp Prog): x3 <= x6
solver.Add(x[3] <= x[6])

# To take c5 (Comp Sim), must take c6 (Comp Prog): x5 <= x6
solver.Add(x[5] <= x[6])

# To take c4 (Mgr Stats), must take c1 (Calculus): x4 <= x1
solver.Add(x[4] <= x[1])

# To take c7 (Forecasting), must take c4 (Mgr Stats): x7 <= x4
solver.Add(x[7] <= x[4])

# Objective: Minimize total number of courses
obj = sum(x[i] for i in range(1, 8))
solver.Minimize(obj)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")