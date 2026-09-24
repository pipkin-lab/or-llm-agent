from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Index set K = {1, 2, 3, 4}
K = [1, 2, 3, 4]

# Parameters
I0 = 500
C = 1000
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

# Decision variables
x = dict()
y = dict()
I = dict()
for k in K:
    x[k] = solver.IntVar(0, INF, 'x_' + str(k))
    y[k] = solver.IntVar(0, INF, 'y_' + str(k))
    I[k] = solver.IntVar(0, INF, 'I_' + str(k))

# Objective: Maximize total revenue - total purchase cost
obj_terms = []
for k in K:
    obj_terms.append(s[k] * y[k])
for k in K:
    obj_terms.append(-b[k] * x[k])
obj = sum(obj_terms)
solver.Maximize(obj)

# Inventory balance constraints
# Month 1: I_1 = I_0 - y_1
solver.Add(I[1] == I0 - y[1])
# Month 2: I_2 = I_1 + x_1 - y_2
solver.Add(I[2] == I[1] + x[1] - y[2])
# Month 3: I_3 = I_2 + x_2 - y_3
solver.Add(I[3] == I[2] + x[2] - y[3])
# Month 4: I_4 = I_3 + x_3 - y_4
solver.Add(I[4] == I[3] + x[3] - y[4])

# Warehouse capacity constraints
for k in K:
    solver.Add(I[k] <= C)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")