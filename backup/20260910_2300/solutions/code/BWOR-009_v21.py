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

T = [1, 2, 3, 4]

# Decision variables
x = dict()
I = dict()
for t in T:
    x[t] = solver.IntVar(0, C[t], 'x_' + str(t))
    I[t] = solver.IntVar(0, INF, 'I_' + str(t))

# Objective
obj = 0
for t in T:
    obj += p[t] * x[t] + h * I[t]

solver.Minimize(obj)

# Inventory balance constraints
# I_t = I_{t-1} + x_t - D_t
for t in T:
    if t == 1:
        solver.Add(I[1] == x[1] - D[1])
    else:
        solver.Add(I[t] == I[t - 1] + x[t] - D[t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")