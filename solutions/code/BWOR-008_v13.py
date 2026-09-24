from ortools.linear_solver import pywraplp

# Parameter definitions
routes = [1, 2, 3, 4]
f = {1: 3, 2: 2, 3: 1, 4: 1}

# Cost matrix C[r][s] = T_{D_r, O_s}
C = dict()
C[1, 1] = 17
C[1, 2] = 13
C[1, 3] = 14
C[1, 4] = 0
C[2, 1] = 5
C[2, 2] = 3
C[2, 3] = 2
C[2, 4] = 15
C[3, 1] = 3
C[3, 2] = 8
C[3, 3] = 7
C[3, 4] = 20
C[4, 1] = 8
C[4, 2] = 0
C[4, 3] = 1
C[4, 4] = 13

# Constant service workload
const_workload = 91

# Solver initialization (LP -> GLOP)
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: z[r, s] >= 0
z = dict()
for r in routes:
    for s in routes:
        z[r, s] = solver.NumVar(0, INF, 'z_' + str(r) + '_' + str(s))

# Flow conservation constraints (inflow)
for r in routes:
    inflow = sum(z[s, r] for s in routes)
    solver.Add(inflow == f[r], 'inflow_r' + str(r))

# Flow conservation constraints (outflow)
for r in routes:
    outflow = sum(z[r, s] for s in routes)
    solver.Add(outflow == f[r], 'outflow_r' + str(r))

# Objective: Minimize const_workload + sum z[r,s] * C[r,s]
obj = const_workload
for r in routes:
    for s in routes:
        obj += z[r, s] * C[r, s]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")