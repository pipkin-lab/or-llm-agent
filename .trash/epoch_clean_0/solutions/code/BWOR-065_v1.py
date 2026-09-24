from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
T = range(6)
D = [1, 2, 5, 3, 2, 1]
C_max = 4
S_max = 3
C_prod = 10000
F = 4000
C_hold = 1000
I0 = 0

# Decision Variables
x = dict()
I = dict()
y = dict()

for t in T:
    x[t] = solver.NumVar(0, solver.infinity(), 'x_' + str(t))
    I[t] = solver.NumVar(0, solver.infinity(), 'I_' + str(t))
    y[t] = solver.BoolVar('y_' + str(t))

# Objective Function
obj = 0
for t in T:
    obj += C_prod * x[t] + F * y[t]
for t in range(5):
    obj += C_hold * I[t]

solver.Minimize(obj)

# A. Inventory Balance Constraints
# I_1 = I_0 + x_1 - D_1
solver.Add(I[0] == I0 + x[0] - D[0])
for t in range(1, 6):
    solver.Add(I[t] == I[t - 1] + x[t] - D[t])

# I_6 = 0
solver.Add(I[5] == 0)

# B. Production Capacity Constraints
for t in T:
    solver.Add(x[t] <= C_max)

# C. Warehouse Storage Capacity Constraints
for t in range(5):
    solver.Add(I[t] <= S_max)

# D. Linking Constraints
for t in T:
    solver.Add(x[t] <= C_max * y[t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")