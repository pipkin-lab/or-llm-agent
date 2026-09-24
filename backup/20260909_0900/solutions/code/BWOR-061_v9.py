from ortools.linear_solver import pywraplp

# Pre-calculated expected values for each strategy
Z = [2.251, 2.236, 2.336, 2.296]
n_strategies = len(Z)

# Create solver (MILP since we have binary variables)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: y_m for each strategy m
y = dict()
for m in range(n_strategies):
    y[m] = solver.BoolVar('y_' + str(m))

# Constraint: exactly one strategy must be chosen
solver.Add(sum(y[m] for m in range(n_strategies)) == 1)

# Objective: Maximize expected score
obj = sum(Z[m] * y[m] for m in range(n_strategies))
solver.Maximize(obj)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")