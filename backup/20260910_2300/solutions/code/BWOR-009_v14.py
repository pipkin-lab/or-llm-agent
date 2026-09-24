from ortools.linear_solver import pywraplp

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

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables
x = dict()
I = dict()
for t in T:
    x[t] = solver.IntVar(0, solver.infinity(), 'x_' + str(t))
    I[t] = solver.IntVar(0, solver.infinity(), 'I_' + str(t))

# Production capacity constraints
for t in T:
    solver.Add(x[t] <= C[t])

# Inventory balance constraints
# I_t = I_{t-1} + x_t - D_t, with I_0 = 0
solver.Add(I[1] == 0 + x[1] - D[1])
solver.Add(I[2] == I[1] + x[2] - D[2])
solver.Add(I[3] == I[2] + x[3] - D[3])
solver.Add(I[4] == I[3] + x[4] - D[4])

# Objective function: minimize total cost
obj_terms = []
for t in T:
    obj_terms.append(p[t] * x[t])
    obj_terms.append(h * I[t])

solver.Minimize(sum(obj_terms))

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")