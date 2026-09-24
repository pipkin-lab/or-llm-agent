from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Index Sets
K = ['A', 'B', 'C', 'D', 'E']
J = [1, 2, 3, 4]

# Parameters
D = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 8}
C = {1: 2, 2: 6, 3: 8, 4: 11}
# Since specific costs c_j are not provided numerically, we assume a standard scenario
# where costs are distinct positive integers to allow for a unique optimal solution structure,
# or we can set them to 1 if the problem implies minimizing number of trucks.
# However, the prompt says "c_1, c_2, c_3, c_4 are given cost parameters" but doesn't list values.
# In such cases for coding tasks, if values are missing, we often assume 1 or look for context.
# Let's assume c_j = 1 for all j as a default "minimum number of trucks" interpretation, 
# or perhaps the costs are proportional to capacity? 
# Looking at similar problems, often if costs aren't given, it's a feasibility or min-truck problem.
# Let's assume c_j = 1 for simplicity, or we can define them as variables? No, they are parameters.
# Let's assume c = {1: 1, 2: 1, 3: 1, 4: 1} to minimize the number of trucks used.
# If specific costs were intended, they would usually be listed. Without them, 1 is the standard fallback for "cost per truck".
c = {1: 1, 2: 1, 3: 1, 4: 1}

# Decision Variables
# x[k][j] is 1 if truck j serves customer k
x = dict()
for k in K:
    for j in J:
        x[k, j] = solver.IntVar(0, 1, 'x_' + k + '_' + str(j))

# y[j] is 1 if truck j is used
y = dict()
for j in J:
    y[j] = solver.IntVar(0, 1, 'y_' + str(j))

# Objective Function: Minimize total cost
obj = 0
for j in J:
    obj += c[j] * y[j]
solver.Minimize(obj)

# Constraints

# 1. Customer Demand Satisfaction: Each customer served by exactly one truck
for k in K:
    solver.Add(sum(x[k, j] for j in J) == 1)

# 2. Truck Capacity Constraints
for j in J:
    solver.Add(sum(D[k] * x[k, j] for k in K) <= C[j] * y[j])

# 3. Linking Constraints: If x[k,j] is 1, then y[j] must be 1
for k in K:
    for j in J:
        solver.Add(y[j] >= x[k, j])

# 4. Incompatibility Constraints
# A and C cannot be on the same truck
for j in J:
    solver.Add(x['A', j] + x['C', j] <= 1)

# B and D cannot be on the same truck
for j in J:
    solver.Add(x['B', j] + x['D', j] <= 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")