from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

months = [1, 2, 3, 4]

# Parameters
b = dict()
b[1] = 10
b[2] = 9
b[3] = 11
b[4] = 15

s = dict()
s[1] = 12
s[2] = 9
s[3] = 13
s[4] = 17

I0 = 500
C = 1000

# Decision variables
x = dict()
y = dict()
I = dict()

for k in months:
    x[k] = solver.IntVar(0, INF, 'x_' + str(k))
    y[k] = solver.IntVar(0, INF, 'y_' + str(k))
    I[k] = solver.IntVar(0, INF, 'I_' + str(k))

# Objective: maximize sum(s_k * y_k - b_k * x_k)
obj = 0
for k in months:
    obj += s[k] * y[k] - b[k] * x[k]
solver.Maximize(obj)

# Sales availability constraints
solver.Add(y[1] <= I0)
for k in [2, 3, 4]:
    solver.Add(y[k] <= I[k - 1])

# Inventory balance constraints
solver.Add(I[1] == I0 - y[1] + x[1])
solver.Add(I[2] == I[1] - y[2] + x[2])
solver.Add(I[3] == I[2] - y[3] + x[3])
solver.Add(I[4] == I[3] - y[4] + x[4])

# Capacity constraints
for k in months:
    solver.Add(I[k] <= C)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")