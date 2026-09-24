from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x[k] for k in 1..7 (1-indexed)
x = dict()
for k in range(1, 8):
    x[k] = solver.IntVar(0, INF, 'x_' + str(k))

# Helper: get x with 1-indexed modular arithmetic (indices mod 7, mapping to 1..7)
# x[i] where i is 1-indexed; for i <= 0 or i > 7, wrap around
def get_x(i):
    # Convert to 0-indexed for mod, then back to 1-indexed
    idx = ((i - 1) % 7) + 1
    return x[idx]

# Requirements
req_6_10 = 18
req_10_14 = 20
req_14_18 = 19
req_18_22 = 17
req_22_6 = 12

# Constraints for each day d in 1..7
for d in range(1, 8):
    # 1. 6:00-10:00: x_d + x_{d-1} >= 18
    solver.Add(get_x(d) + get_x(d - 1) >= req_6_10)
    
    # 2. 10:00-14:00: x_{d-1} + x_{d-2} >= 20
    solver.Add(get_x(d - 1) + get_x(d - 2) >= req_10_14)
    
    # 3. 14:00-18:00: x_{d-2} + x_{d-3} >= 19
    solver.Add(get_x(d - 2) + get_x(d - 3) >= req_14_18)
    
    # 4. 18:00-22:00: x_{d-3} + x_{d-4} >= 17
    solver.Add(get_x(d - 3) + get_x(d - 4) >= req_18_22)
    
    # 5. 22:00-6:00: x_{d-5} + x_d >= 12
    solver.Add(get_x(d - 5) + get_x(d) >= req_22_6)

# Objective: Minimize total nurses
objective = sum(x[k] for k in range(1, 8))
solver.Minimize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")