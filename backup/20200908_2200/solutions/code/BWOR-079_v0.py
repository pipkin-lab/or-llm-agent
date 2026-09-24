from ortools.linear_solver import pywraplp

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
D = range(1, 8)  # Days 1 to 7 (Monday to Sunday)
requirements = [18, 20, 19, 17, 12]  # Minimum nurses for periods 1 to 5

# Decision Variables
# x[d] is the number of nurses starting their 5-day cycle on day d
x = {}
for d in D:
    x[d] = solver.IntVar(0, solver.infinity(), f'x_{d}')

# Objective Function: Minimize total nurses
solver.Minimize(sum(x[d] for d in D))

# Helper function to get index modulo 7 (1-based indexing)
# d is 1-based. We want (d - offset) mod 7, mapping 0 to 7.
def get_idx(d, offset):
    # d is 1..7
    # We want the day that is 'offset' days before 'd' in the cycle.
    # e.g., if d=1 (Mon), offset=1, we want Sun (7).
    # (1 - 1) % 7 = 0 -> 0 + 7 = 7. Correct.
    # if d=2 (Tue), offset=1, we want Mon (1).
    # (2 - 1) % 7 = 1 -> 1. Correct.
    # if d=1 (Mon), offset=4, we want Thu (4).
    # (1 - 4) % 7 = -3 % 7 = 4. Correct.
    idx = (d - offset) % 7
    if idx == 0:
        return 7
    return idx

# Constraints
for d in D:
    # Period 1 (6-10): Covered by Shift 1 (x_d) and Shift 2 (x_{d-1})
    # Requirement: >= 18
    solver.Add(x[d] + x[get_idx(d, 1)] >= requirements[0])
    
    # Period 2 (10-14): Covered by Shift 2 (x_{d-1}) and Shift 3 (x_{d-2})
    # Requirement: >= 20
    solver.Add(x[get_idx(d, 1)] + x[get_idx(d, 2)] >= requirements[1])
    
    # Period 3 (14-18): Covered by Shift 3 (x_{d-2}) and Shift 4 (x_{d-3})
    # Requirement: >= 19
    solver.Add(x[get_idx(d, 2)] + x[get_idx(d, 3)] >= requirements[2])
    
    # Period 4 (18-22): Covered by Shift 4 (x_{d-3}) and Shift 5 (x_{d-4})
    # Requirement: >= 17
    solver.Add(x[get_idx(d, 3)] + x[get_idx(d, 4)] >= requirements[3])
    
    # Period 5 (22-6): Covered by Shift 5 (x_{d-4}) and Shift 1 (x_d)
    # Requirement: >= 12
    solver.Add(x[get_idx(d, 4)] + x[d] >= requirements[4])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
    # Optional: Print individual variable values for debugging/verification
    # for d in D:
    #     print(f"x_{d} = {x[d].solution_value()}")
else:
    print("NO_FEASIBLE_SOLUTION")