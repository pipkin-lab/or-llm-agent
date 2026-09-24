from ortools.linear_solver import pywraplp

# Initialize solver (MILP since variables are integer)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
T = 4
C = dict()
C[0] = 25
C[1] = 35
C[2] = 30
C[3] = 20

D = dict()
D[0] = 15
D[1] = 20
D[2] = 25
D[3] = 20

p = dict()
p[0] = 12.0
p[1] = 11.0
p[2] = 11.5
p[3] = 12.5

h = 0.1

# Decision variables
x = dict()
I = dict()
for t in range(T):
    x[t] = solver.IntVar(0, solver.infinity(), 'x_' + str(t + 1))
    I[t] = solver.IntVar(0, solver.infinity(), 'I_' + str(t + 1))

# Objective function
obj = 0
for t in range(T):
    obj += p[t] * x[t] + h * I[t]

# Constraints
# Inventory balance: I_t = I_{t-1} + x_t - D_t, with I_0 = 0
solver.Add(I[0] == 0 + x[0] - D[0])
solver.Add(I[1] == I[0] + x[1] - D[1])
solver.Add(I[2] == I[1] + x[2] - D[2])
solver.Add(I[3] == I[2] + x[3] - D[3])

# Capacity constraints
solver.Add(x[0] <= C[0])
solver.Add(x[1] <= C[1])
solver.Add(x[2] <= C[2])
solver.Add(x[3] <= C[3])

# Final inventory must be zero
solver.Add(I[3] == 0)

# Solve
solver.Minimize(obj)
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")