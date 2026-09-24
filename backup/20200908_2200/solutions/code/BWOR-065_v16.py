from ortools.linear_solver import pywraplp

# Create the solver (MILP due to binary variables y_t)
solver = pywraplp.Solver.CreateSolver('SCIP')

T = [1, 2, 3, 4, 5, 6]
D = {1: 1, 2: 2, 3: 5, 4: 3, 5: 2, 6: 1}
C_cap = 4
W_cap = 3
c_v = 10
c_f = 4
h = 1

# Decision variables
x = dict()
y = dict()
I = dict()

for t in T:
    x[t] = solver.NumVar(0, solver.infinity(), 'x_' + str(t))
    y[t] = solver.BoolVar('y_' + str(t))
    I[t] = solver.NumVar(0, W_cap, 'I_' + str(t))

# Objective
obj = 0
for t in T:
    obj += c_v * x[t] + c_f * y[t] + h * I[t]

solver.Minimize(obj)

# Inventory balance constraints
# t=1: I_0 + x_1 - D_1 = I_1, I_0 = 0
solver.Add(x[1] - D[1] == I[1])
# t=2 to 5
for t in [2, 3, 4, 5]:
    solver.Add(I[t-1] + x[t] - D[t] == I[t])
# t=6: I_5 + x_6 - D_6 = I_6 = 0
solver.Add(I[5] + x[6] - D[6] == 0)

# Production capacity and fixed cost linking
for t in T:
    solver.Add(x[t] <= C_cap * y[t])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")