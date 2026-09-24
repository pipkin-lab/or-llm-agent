from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
d = dict()
d[1] = 3
d[2] = 3
d[3] = 3

N = dict()
N[1] = 2
N[2] = 4
N[3] = 1

O = dict()
O[1] = 3
O[2] = 2
O[3] = 3

c = dict()
c[1] = 500
c[2] = 600
c[3] = 550

p = 70
h = 40
I0 = 2

# Decision Variables
x = dict()
y = dict()
I = dict()

for t in range(1, 4):
    x[t] = solver.IntVar(0, N[t], 'x_' + str(t))
    y[t] = solver.IntVar(0, O[t], 'y_' + str(t))
    I[t] = solver.IntVar(0, solver.infinity(), 'I_' + str(t))

# Inventory Balance Constraints
for t in range(1, 4):
    if t == 1:
        solver.Add(I[t] == I0 + x[t] + y[t] - d[t])
    else:
        solver.Add(I[t] == I[t - 1] + x[t] + y[t] - d[t])

# Final Inventory Requirement
solver.Add(I[3] == 1)

# Objective Function
obj = 0
for t in range(1, 4):
    obj += c[t] * x[t] + (c[t] + p) * y[t] + h * I[t]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")