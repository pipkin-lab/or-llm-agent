from ortools.linear_solver import pywraplp

# Check if cost parameters are provided
c_values = None  # c_1, c_2, c_3, c_4 not provided in the problem text

if c_values is None:
    raise ValueError("Truck cost parameters c_1, c_2, c_3, c_4 are not provided in the model. "
                     "Please provide numeric values for the cost of using each truck.")

# Index sets
customers = ['A', 'B', 'C', 'D', 'E']
trucks = [1, 2, 3, 4]
forbidden_pairs = [('A', 'C'), ('B', 'D')]

# Parameters
q = dict()
q['A'] = 1
q['B'] = 2
q['C'] = 3
q['D'] = 4
q['E'] = 8

u = dict()
u[1] = 2
u[2] = 6
u[3] = 8
u[4] = 11

c = dict()
c[1] = c_values[0]
c[2] = c_values[1]
c[3] = c_values[2]
c[4] = c_values[3]

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for i in customers:
    for j in trucks:
        x[i, j] = solver.BoolVar('x_' + i + '_' + str(j))

y = dict()
for j in trucks:
    y[j] = solver.BoolVar('y_' + str(j))

# Objective: minimize sum c_j * y_j
obj = 0
for j in trucks:
    obj += c[j] * y[j]
solver.Minimize(obj)

# Constraint 1: Each customer assigned to exactly one truck
for i in customers:
    solver.Add(sum(x[i, j] for j in trucks) == 1)

# Constraint 2: Truck capacity
for j in trucks:
    solver.Add(sum(q[i] * x[i, j] for i in customers) <= u[j])

# Constraint 3: Forbidden pairs
for (i1, i2) in forbidden_pairs:
    for j in trucks:
        solver.Add(x[i1, j] + x[i2, j] <= 1)

# Constraint 4: Linking constraints
for i in customers:
    for j in trucks:
        solver.Add(x[i, j] <= y[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")