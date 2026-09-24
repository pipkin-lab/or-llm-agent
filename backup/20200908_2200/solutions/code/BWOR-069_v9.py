from ortools.linear_solver import pywraplp

# Create the solver (MILP -> SCIP)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
weights = [2, 3, 4]   # w_1, w_2, w_3
profits = [100, 140, 180]  # p_1, p_2, p_3
W_max = 10

# Decision variables: x_1, x_2, x_3 (non-negative integers)
x = dict()
for i in range(3):
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i + 1))

# Capacity constraint: 2*x_1 + 3*x_2 + 4*x_3 <= 10
solver.Add(2 * x[0] + 3 * x[1] + 4 * x[2] <= W_max)

# Objective: Maximize 100*x_1 + 140*x_2 + 180*x_3
objective = 100 * x[0] + 140 * x[1] + 180 * x[2]
solver.Maximize(objective)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")