from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
C_FT = 80
C_CT = 120
R = [10, 15, 25, 20, 18, 12]  # R[0] corresponds to t=1, R[1] to t=2, etc.

# Number of shifts
n_shifts = 6

# Decision Variables
# x[s]: Number of full-time nurses for shift s (0-indexed: 0..5)
# y[s]: Number of contract nurses for shift s (0-indexed: 0..5)
x = dict()
y = dict()

for s in range(n_shifts):
    x[s] = solver.IntVar(0, solver.infinity(), 'x_' + str(s))
    y[s] = solver.IntVar(0, solver.infinity(), 'y_' + str(s))

# Objective Function
# Minimize total cost
obj = sum((C_FT * x[s] + C_CT * y[s]) for s in range(n_shifts))
solver.Minimize(obj)

# Coverage Constraints
# Period t (1-based) is covered by shift s if:
# s == t (shift starts at period t) OR s == t-1 (shift started at previous period, covering current)
# In 0-based indexing:
# Period t_idx (0..5) corresponds to time period t = t_idx + 1
# Shift s_idx (0..5) corresponds to shift start s = s_idx + 1
#
# Coverage logic:
# Period 1 (idx 0): Shift 1 (idx 0) and Shift 6 (idx 5)
# Period 2 (idx 1): Shift 1 (idx 0) and Shift 2 (idx 1)
# Period 3 (idx 2): Shift 2 (idx 1) and Shift 3 (idx 2)
# Period 4 (idx 3): Shift 3 (idx 2) and Shift 4 (idx 3)
# Period 5 (idx 4): Shift 4 (idx 3) and Shift 5 (idx 4)
# Period 6 (idx 5): Shift 5 (idx 4) and Shift 6 (idx 5)
#
# General rule for period index t_idx (0-based):
# Covered by shift (t_idx) and shift (t_idx - 1) mod 6

for t_idx in range(n_shifts):
    # The shift that starts at this period
    s1 = t_idx
    # The shift that started at the previous period (wraps around)
    s2 = (t_idx - 1) % n_shifts
    
    # Constraint: x[s1] + y[s1] + x[s2] + y[s2] >= R[t_idx]
    solver.Add(x[s1] + y[s1] + x[s2] + y[s2] >= R[t_idx])

# Solve the model
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")