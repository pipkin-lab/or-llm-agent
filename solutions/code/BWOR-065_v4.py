from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Parameters
months = [1, 2, 3, 4, 5, 6]
D = dict()
D[1] = 100
D[2] = 200
D[3] = 500
D[4] = 300
D[5] = 200
D[6] = 100

P_max = 400
I_max = 300
c_prod = 100
F = 4000
c_hold = 10
I0 = 0
I6 = 0

# Decision Variables
x = dict()
y = dict()
I = dict()

for t in months:
    x[t] = solver.IntVar(0, P_max, 'x_' + str(t))
    y[t] = solver.BoolVar('y_' + str(t))

for t in range(1, 6):
    I[t] = solver.IntVar(0, I_max, 'I_' + str(t))

# Objective
obj = 0
for t in months:
    obj += c_prod * x[t] + F * y[t]
for t in range(1, 6):
    obj += c_hold * I[t]

solver.Minimize(obj)

# Constraints

# 1. Linking production and fixed cost
for t in months:
    solver.Add(x[t] <= P_max * y[t])

# 2. Inventory balance
for t in months:
    if t == 1:
        solver.Add(I0 + x[1] - D[1] == I[1])
    elif t == 6:
        solver.Add(I[5] + x[6] - D[6] == I6)
    else:
        solver.Add(I[t - 1] + x[t] - D[t] == I[t])

# 3. Warehouse capacity (already enforced by variable bounds)

# 4. Production capacity (already enforced by variable bounds)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")