from ortools.linear_solver import pywraplp

# Initialize MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Parameters
K = [1, 2, 3, 4]
B = dict()
B[1] = 10
B[2] = 9
B[3] = 11
B[4] = 15

S = dict()
S[1] = 12
S[2] = 9
S[3] = 13
S[4] = 17

W = 1000
I0 = 500

# Decision variables
x = dict()
y = dict()
I = dict()

for k in K:
    x[k] = solver.IntVar(0, INF, 'x_' + str(k))
    y[k] = solver.IntVar(0, INF, 'y_' + str(k))
    I[k] = solver.IntVar(0, INF, 'I_' + str(k))

# Objective: Maximize total profit
obj = 0
for k in K:
    obj += S[k] * y[k] - B[k] * x[k]
solver.Maximize(obj)

# Constraints

# 1. Inventory balance: I_k = I_{k-1} + x_k - y_k
for k in K:
    if k == 1:
        solver.Add(I[1] == I0 + x[1] - y[1])
    else:
        solver.Add(I[k] == I[k - 1] + x[k] - y[k])

# 2. Sales limited by start-of-month inventory: y_k <= I_{k-1}
for k in K:
    if k == 1:
        solver.Add(y[1] <= I0)
    else:
        solver.Add(y[k] <= I[k - 1])

# 3. Warehouse capacity: I_k <= W
for k in K:
    solver.Add(I[k] <= W)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")