from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
inf = solver.infinity()

# Parameters
D = [None, 1, 2, 5, 3, 2, 1]  # Demand for months 1 to 6
C_cap = 4
I_cap = 3
c_v = 100
c_f = 4000
c_h = 10

# Decision Variables
# x[t]: Production quantity in month t (continuous, >= 0)
# I[t]: Inventory at end of month t (continuous, >= 0)
# y[t]: Binary variable indicating if production occurs in month t
x = dict()
I = dict()
y = dict()

for t in range(1, 7):
    x[t] = solver.NumVar(0, inf, 'x_' + str(t))
    I[t] = solver.NumVar(0, inf, 'I_' + str(t))
    y[t] = solver.BoolVar('y_' + str(t))

# Objective Function
# Minimize sum of (c_v * x[t] + c_f * y[t] + c_h * I[t])
obj_terms = []
for t in range(1, 7):
    obj_terms.append(c_v * x[t] + c_f * y[t] + c_h * I[t])

solver.Minimize(sum(obj_terms))

# Constraints

# 1. Inventory Balance Constraints
# I[t] = I[t-1] + x[t] - D[t], with I[0] = 0
for t in range(1, 7):
    if t == 1:
        # I[1] = 0 + x[1] - D[1] => I[1] - x[1] = -D[1]
        solver.Add(I[1] - x[1] == -D[1])
    else:
        # I[t] - I[t-1] - x[t] = -D[t]
        solver.Add(I[t] - I[t-1] - x[t] == -D[t])

# 2. End-of-Horizon Inventory Constraint
# I[6] = 0
solver.Add(I[6] == 0)

# 3. Production Capacity Constraints
# x[t] <= C_cap * y[t]
for t in range(1, 7):
    solver.Add(x[t] <= C_cap * y[t])

# 4. Warehouse Storage Capacity Constraints
# I[t] <= I_cap
for t in range(1, 7):
    solver.Add(I[t] <= I_cap)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")