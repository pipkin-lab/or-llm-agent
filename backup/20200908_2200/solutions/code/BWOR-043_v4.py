from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
I = range(4)  # Sources 0 to 3
J = range(6)  # Destinations 0 to 5

supply = [50, 40, 60, 31]
demand = [30, 50, 20, 40, 30, 11]

# Cost matrix c[i][j]
cost = [
    [2, 1, 3, 3, 3, 5],  # Source 1 (A1)
    [4, 2, 2, 4, 4, 4],  # Source 2 (A2)
    [3, 5, 4, 2, 4, 1],  # Source 3 (A3)
    [4, 2, 2, 1, 2, 2]   # Source 4 (A4)
]

# Decision variables x[i][j]
x = {}
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_{}_{}'.format(i, j))

# Objective function: minimize total cost
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(cost[i][j] * x[i, j])

solver.Minimize(sum(obj_terms))

# Supply constraints: outflow from each source <= supply[i]
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= supply[i])

# Demand constraints: inflow to each destination == demand[j]
for j in J:
    solver.Add(sum(x[i, j] for i in I) == demand[j])

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")