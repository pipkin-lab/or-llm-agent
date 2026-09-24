from ortools.linear_solver import pywraplp

# Initialize the solver (ILP -> SCIP)
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision Variables: N_j for j in 1..7 (nurses starting 5-day cycle on day j)
N = dict()
for j in range(1, 8):
    N[j] = solver.IntVar(0, INF, 'N_' + str(j))

# Demand parameters
demand = dict()
demand[1] = 18
demand[2] = 20
demand[3] = 19
demand[4] = 17
demand[5] = 12

# Helper to get index mod 7 (1-indexed)
def mod7(k):
    r = k % 7
    if r == 0:
        return 7
    return r

# Constraints
for d in range(1, 8):
    # Period 1: N_d + N_{d-1} >= 18
    idx_d = d
    idx_dm1 = mod7(d - 1)
    solver.Add(N[idx_d] + N[idx_dm1] >= demand[1])

    # Period 2: N_{d-1} + N_{d-2} >= 20
    idx_dm1 = mod7(d - 1)
    idx_dm2 = mod7(d - 2)
    solver.Add(N[idx_dm1] + N[idx_dm2] >= demand[2])

    # Period 3: N_{d-2} + N_{d-3} >= 19
    idx_dm2 = mod7(d - 2)
    idx_dm3 = mod7(d - 3)
    solver.Add(N[idx_dm2] + N[idx_dm3] >= demand[3])

    # Period 4: N_{d-3} + N_{d-4} >= 17
    idx_dm3 = mod7(d - 3)
    idx_dm4 = mod7(d - 4)
    solver.Add(N[idx_dm3] + N[idx_dm4] >= demand[4])

    # Period 5a: N_{d-4} >= 12
    idx_dm4 = mod7(d - 4)
    solver.Add(N[idx_dm4] >= demand[5])

    # Period 5b: N_{d+1} >= 12
    idx_dp1 = mod7(d + 1)
    solver.Add(N[idx_dp1] >= demand[5])

# Objective: Minimize total nurses
obj = 0
for j in range(1, 8):
    obj += N[j]

solver.Minimize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")