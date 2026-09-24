from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
f = dict()
f[1] = 3
f[2] = 2
f[3] = 1
f[4] = 1

T = dict()
T[1] = 36
T[2] = 8
T[3] = 16
T[4] = 28

routes = [1, 2, 3, 4]

# Decision variable
N = solver.IntVar(0, solver.infinity(), 'N')

# Objective: minimize N
solver.Minimize(N)

# Constraint: N >= sum(f_r * T_r)
total_workload = sum(f[r] * T[r] for r in routes)
solver.Add(N >= total_workload)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")