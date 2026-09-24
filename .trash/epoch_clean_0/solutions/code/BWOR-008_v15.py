from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters from the mathematical model
# Route frequencies (sailings per day)
f = dict()
f[1] = 3  # Route 1: E -> D
f[2] = 2  # Route 2: B -> C
f[3] = 1  # Route 3: A -> F
f[4] = 1  # Route 4: D -> B

# Sailing times (one-way) in days
t_od = dict()
t_od[1] = 17  # E -> D
t_od[2] = 3   # B -> C
t_od[3] = 7   # A -> F
t_od[4] = 13  # D -> B

# Return sailing times (destination to origin) in days
t_do = dict()
t_do[1] = 17  # D -> E
t_do[2] = 3   # C -> B
t_do[3] = 7   # F -> A
t_do[4] = 13  # B -> D

# Port times
t_load = 1
t_unload = 1

# Compute total workload (ship-days per day)
# W = sum over routes of f_r * (t_load + t_od_r + t_unload + t_do_r)
total_workload = 0
for r in [1, 2, 3, 4]:
    T_r = t_load + t_od[r] + t_unload + t_do[r]
    total_workload += f[r] * T_r

# Decision variable: N = total number of ships (integer, >= 0)
N = solver.IntVar(0, solver.infinity(), 'N')

# Objective: Minimize N
solver.Minimize(N)

# Constraint: N >= total_workload
solver.Add(N >= total_workload)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")