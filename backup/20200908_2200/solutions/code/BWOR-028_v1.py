from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
# Minimum number of nurses required during each period
d = {
    0: 10,  # Period 1: 2:00 - 6:00
    1: 15,  # Period 2: 6:00 - 10:00
    2: 25,  # Period 3: 10:00 - 14:00
    3: 20,  # Period 4: 14:00 - 18:00
    4: 18,  # Period 5: 18:00 - 22:00
    5: 12   # Period 6: 22:00 - 2:00
}

# Number of shifts/periods
N = 6

# Decision Variables
# x_s: Number of nurses starting shift s (0 to 5 corresponding to shifts 1 to 6)
x = {}
for s in range(N):
    x[s] = solver.IntVar(0, solver.infinity(), f'x_{s}')

# Constraints
# a_{p,s} = 1 if shift s covers period p
# Shift s (0-indexed) starts at period s and covers period s and (s+1)%N
# Therefore, period p is covered by shift p (starting at p) and shift (p-1)%N (starting at p-1)

# Period 0 (2:00-6:00): Covered by Shift 0 (starts 2:00) and Shift 5 (starts 22:00 prev day)
solver.Add(x[0] + x[5] >= d[0])

# Period 1 (6:00-10:00): Covered by Shift 1 (starts 6:00) and Shift 0 (starts 2:00)
solver.Add(x[1] + x[0] >= d[1])

# Period 2 (10:00-14:00): Covered by Shift 2 (starts 10:00) and Shift 1 (starts 6:00)
solver.Add(x[2] + x[1] >= d[2])

# Period 3 (14:00-18:00): Covered by Shift 3 (starts 14:00) and Shift 2 (starts 10:00)
solver.Add(x[3] + x[2] >= d[3])

# Period 4 (18:00-22:00): Covered by Shift 4 (starts 18:00) and Shift 3 (starts 14:00)
solver.Add(x[4] + x[3] >= d[4])

# Period 5 (22:00-2:00): Covered by Shift 5 (starts 22:00) and Shift 4 (starts 18:00)
solver.Add(x[5] + x[4] >= d[5])

# Objective Function: Minimize total number of nurses
solver.Minimize(sum(x[s] for s in range(N)))

# Solve the problem
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
    for s in range(N):
        print(f"x_{s}: {x[s].solution_value()}")
else:
    print("NO_FEASIBLE_SOLUTION")