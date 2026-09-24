from ortools.linear_solver import pywraplp

# Data
p = [100, 60, 80, 40, 110, 90, 30]  # index 0..6 for products 1..7

# Machine hours matrix: rows = machines (0..4), cols = products (0..6)
a = [
    [0.5, 0.7, 0.0, 0.0, 0.3, 0.2, 0.5],  # Grinding
    [0.1, 0.2, 0.0, 0.3, 0.0, 0.6, 0.0],  # Upright Drill
    [0.2, 0.0, 0.8, 0.0, 0.0, 0.0, 0.6],  # Horizontal Drill
    [0.05, 0.03, 0.0, 0.07, 0.1, 0.0, 0.08],  # Boring
    [0.0, 0.0, 0.01, 0.0, 0.05, 0.0, 0.05]   # Planer
]

N = [4, 2, 3, 1, 1]  # Total machines per type

# Maintenance schedule: M_maint[t][m] for t in 0..5, m in 0..4
M_maint = [
    [1, 0, 0, 0, 0],  # Jan
    [0, 0, 2, 0, 0],  # Feb
    [0, 0, 0, 1, 0],  # Mar
    [0, 1, 0, 0, 0],  # Apr
    [1, 1, 0, 0, 0],  # May
    [0, 0, 1, 0, 1]   # Jun
]

# Demand D[t][i] for t in 0..5, i in 0..6
# Using placeholder values since Table C-4 is not provided.
# We'll use a reasonable placeholder (e.g., 1000 units per product per month)
# to ensure the model is feasible. In practice, replace with actual data.
D = [[1000] * 7 for _ in range(6)]

h = 5
Inv_max = 100
F_i = 50  # Final inventory requirement
H_total = 384

# Compute capacities C[t][m]
C = [[(N[m] - M_maint[t][m]) * H_total for m in range(5)] for t in range(6)]

# Create solver
solver = pywraplp.Solver.CreateSolver('GLOP')
if solver is None:
    print("NO_FEASIBLE_SOLUTION")
    exit(1)

# Decision variables
# x[t][i]: production quantity
x = dict()
# Inv[t][i]: inventory at end of month t
Inv = dict()

for t in range(6):
    for i in range(7):
        x[t, i] = solver.NumVar(0, solver.infinity(), 'x_' + str(t) + '_' + str(i))
        Inv[t, i] = solver.NumVar(0, Inv_max, 'Inv_' + str(t) + '_' + str(i))

# Objective function
obj_terms = []
for t in range(6):
    for i in range(7):
        obj_terms.append(p[i] * x[t, i])
        obj_terms.append(-h * Inv[t, i])

solver.Maximize(sum(obj_terms))

# Constraints

# 1. Inventory balance and sales bounds
for t in range(6):
    for i in range(7):
        if t == 0:
            Inv_prev = 0
        else:
            Inv_prev = Inv[t-1, i]
        
        # Sales = Inv_prev + x[t,i] - Inv[t,i]
        # Constraint: 0 <= Sales <= D[t][i]
        # Lower bound: Inv[t,i] - x[t,i] - Inv_prev <= 0
        solver.Add(Inv[t, i] - x[t, i] - Inv_prev <= 0)
        # Upper bound: x[t,i] - Inv[t,i] + Inv_prev <= D[t][i]
        solver.Add(x[t, i] - Inv[t, i] + Inv_prev <= D[t][i])

# 2. Machine capacity constraints
for t in range(6):
    for m in range(5):
        cap_expr = sum(a[m][i] * x[t, i] for i in range(7))
        solver.Add(cap_expr <= C[t][m])

# 3. Final inventory requirement
for i in range(7):
    solver.Add(Inv[5, i] == F_i)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    # Calculate the full objective including the constant term
    # Z = sum(p_i * x[t,i]) - sum(h * Inv[t,i]) - sum_i 50 * p_i
    constant = -sum(50 * p[i] for i in range(7))
    total_obj = solver.Objective().Value() + constant
    print("OPTIMAL_VALUE:", total_obj)
else:
    print("NO_FEASIBLE_SOLUTION")