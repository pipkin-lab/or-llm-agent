from ortools.linear_solver import pywraplp

# Create the solver (MILP since variables are integers)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
W = [2, 3, 4]       # Weights in tons
P = [100, 140, 180] # Profits in yuan
C = 10              # Total capacity in tons

# Decision variables: x_i = number of units of product i
x = dict()
for i in range(3):
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

# Objective function: Maximize total profit
obj = sum(P[i] * x[i] for i in range(3))
solver.Maximize(obj)

# Constraint: Total weight <= capacity
solver.Add(2 * x[0] + 3 * x[1] + 4 * x[2] <= C)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")