from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
N = dict()
O = dict()
I = dict()
for t in range(1, 4):
    N[t] = solver.IntVar(0, INF, 'N_' + str(t))
    O[t] = solver.IntVar(0, INF, 'O_' + str(t))
    I[t] = solver.IntVar(0, INF, 'I_' + str(t))

# Production capacity constraints
solver.Add(N[1] <= 2)
solver.Add(O[1] <= 3)
solver.Add(N[2] <= 4)
solver.Add(O[2] <= 2)
solver.Add(N[3] <= 1)
solver.Add(O[3] <= 3)

# Inventory balance constraints (I_0 = 2, D_t = 3)
solver.Add(I[1] == N[1] + O[1] - 1)
solver.Add(I[2] == I[1] + N[2] + O[2] - 3)
solver.Add(I[3] == I[2] + N[3] + O[3] - 3)

# Final inventory constraint
solver.Add(I[3] == 1)

# Objective function: minimize total cost
obj = 500 * N[1] + 570 * O[1] + 600 * N[2] + 670 * O[2] + 550 * N[3] + 620 * O[3] + 40 * (I[1] + I[2] + I[3])
solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")