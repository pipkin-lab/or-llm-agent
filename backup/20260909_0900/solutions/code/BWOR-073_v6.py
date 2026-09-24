from ortools.linear_solver import pywraplp

# Define the solver (MILP since variables are integer)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
N = 12
K = [1, 2, 3, 4]
U = [2, 3, 4]

# Cost table: c[k][u] where k is warehouse index (1-4) and u is units (2-4)
c = {
    1: {2: 18, 3: 16, 4: 12},
    2: {2: 38, 3: 36, 4: 30},
    3: {2: 14, 3: 12, 4: 11},
    4: {2: 34, 3: 31, 4: 25}
}

# Decision variables: u_k for each warehouse k
u = dict()
for k in K:
    u[k] = solver.IntVar(2, 4, 'u_' + str(k))

# Constraint: Total units assigned must equal N
solver.Add(sum(u[k] for k in K) == N)

# Objective: Minimize total expected accidents
# Since c[k][u_k] depends on the value of u_k, we need to linearize this.
# We can introduce binary variables x[k][v] which is 1 if u[k] == v, else 0.
# Then u[k] = sum(v * x[k][v] for v in U)
# And the objective term for warehouse k is sum(c[k][v] * x[k][v] for v in U)

x = dict()
for k in K:
    for v in U:
        x[k, v] = solver.BoolVar('x_' + str(k) + '_' + str(v))

# Link u[k] to x[k][v]
for k in K:
    solver.Add(u[k] == sum(v * x[k, v] for v in U))

# Ensure only one value is selected per warehouse
for k in K:
    solver.Add(sum(x[k, v] for v in U) == 1)

# Objective: Minimize sum of costs
obj = sum(c[k][v] * x[k, v] for k in K for v in U)
solver.Minimize(obj)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")