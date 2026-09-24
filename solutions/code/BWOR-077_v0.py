from ortools.linear_solver import pywraplp

# Parameters
workers = [1, 2, 3, 4, 5]
stations = [1, 2, 3, 4, 5]

# Efficiency matrix e[i, j]
efficiency = dict()
eff_data = {
    1: {1: 2, 2: 3, 3: 4, 4: 1, 5: 7},
    2: {1: 3, 2: 4, 3: 2, 4: 5, 5: 6},
    3: {1: 2, 2: 5, 3: 3, 4: 4, 5: 1},
    4: {1: 5, 2: 2, 3: 3, 4: 2, 5: 5},
    5: {1: 3, 2: 7, 3: 6, 4: 2, 5: 4}
}
for i in workers:
    for j in stations:
        efficiency[i, j] = eff_data[i][j]

# Create MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for i in workers:
    for j in stations:
        x[i, j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

Z = solver.NumVar(0, INF, 'Z')

# Objective: maximize Z
solver.Maximize(Z)

# Constraint 1: Each worker assigned to exactly one station
for i in workers:
    solver.Add(sum(x[i, j] for j in stations) == 1)

# Constraint 2: Each station staffed by exactly one worker
for j in stations:
    solver.Add(sum(x[i, j] for i in workers) == 1)

# Constraint 3: Bottleneck constraints
for j in stations:
    solver.Add(sum(efficiency[i, j] * x[i, j] for i in workers) >= Z)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")