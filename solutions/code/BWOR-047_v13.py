from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

T = [1, 2, 3]

# Parameters
D = dict()
D[1] = 3
D[2] = 3
D[3] = 3

S_N = dict()
S_N[1] = 2
S_N[2] = 4
S_N[3] = 1

S_O = dict()
S_O[1] = 3
S_O[2] = 2
S_O[3] = 3

c_N = dict()
c_N[1] = 500
c_N[2] = 600
c_N[3] = 550

c_O = dict()
c_O[1] = 570
c_O[2] = 670
c_O[3] = 620

h = 40
I_0 = 2
I_final = 1

# Decision variables
x_N = dict()
x_O = dict()
I = dict()

for t in T:
    x_N[t] = solver.IntVar(0, S_N[t], 'x_N_' + str(t))
    x_O[t] = solver.IntVar(0, S_O[t], 'x_O_' + str(t))
    I[t] = solver.IntVar(0, INF, 'I_' + str(t))

# Inventory balance constraints
for t in T:
    if t == 1:
        solver.Add(I[t] == I_0 + x_N[t] + x_O[t] - D[t])
    else:
        solver.Add(I[t] == I[t - 1] + x_N[t] + x_O[t] - D[t])

# Ending inventory requirement
solver.Add(I[3] == I_final)

# Objective
obj = 0
for t in T:
    obj += c_N[t] * x_N[t] + c_O[t] * x_O[t] + h * I[t]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")