from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Parameters
C = dict()
C[1] = 25
C[2] = 35
C[3] = 30
C[4] = 20

D = dict()
D[1] = 15
D[2] = 20
D[3] = 25
D[4] = 20

p = dict()
p[1] = 12.0
p[2] = 11.0
p[3] = 11.5
p[4] = 12.5

h = 0.1

# Decision variables
x = dict()
I = dict()
for t in range(1, 5):
    x[t] = solver.IntVar(0, INF, 'x_' + str(t))
    I[t] = solver.IntVar(0, INF, 'I_' + str(t))

# Inventory balance constraints
# I_1 = x_1 - D_1
solver.Add(I[1] == x[1] - D[1])
# I_2 = I_1 + x_2 - D_2
solver.Add(I[2] == I[1] + x[2] - D[2])
# I_3 = I_2 + x_3 - D_3
solver.Add(I[3] == I[2] + x[3] - D[3])
# I_4 = 0, and I_4 = I_3 + x_4 - D_4
solver.Add(I[3] + x[4] - D[4] == 0)

# Capacity constraints
for t in range(1, 5):
    solver.Add(x[t] <= C[t])

# Objective
obj = sum(p[t] * x[t] for t in range(1, 5)) + h * (I[1] + I[2] + I[3])
solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")