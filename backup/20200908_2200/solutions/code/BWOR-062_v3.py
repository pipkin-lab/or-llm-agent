from ortools.linear_solver import pywraplp

# Define the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    print("Unable to create solver")
    exit(1)

# Index sets
R = [0, 1, 2]  # Regions 1, 2, 3 (using 0-based indexing)
K = [0, 1, 2, 3, 4]  # Possible number of outlets

# Parameters: Profit P[i][k]
# Region 1 (index 0): k=0:0, k=1:16, k=2:25, k=3:30, k=4:32
# Region 2 (index 1): k=0:0, k=1:12, k=2:17, k=3:21, k=4:22
# Region 3 (index 2): k=0:0, k=1:10, k=2:14, k=3:16, k=4:17
P = {
    (0, 0): 0, (0, 1): 16, (0, 2): 25, (0, 3): 30, (0, 4): 32,
    (1, 0): 0, (1, 1): 12, (1, 2): 17, (1, 3): 21, (1, 4): 22,
    (2, 0): 0, (2, 1): 10, (2, 2): 14, (2, 3): 16, (2, 4): 17
}

N = 4  # Total number of sales outlets

# Decision variables: x[i, k] is 1 if k outlets are allocated to region i
x = {}
for i in R:
    for k in K:
        x[i, k] = solver.BoolVar(f'x_{i}_{k}')

# Objective function: Maximize total profit
objective = 0
for i in R:
    for k in K:
        objective += P[(i, k)] * x[i, k]

solver.Maximize(objective)

# Constraint 1: Exactly one allocation state per region
for i in R:
    solver.Add(sum(x[i, k] for k in K) == 1)

# Constraint 2: Total number of outlets allocated must equal N
total_outlets = 0
for i in R:
    for k in K:
        total_outlets += k * x[i, k]
solver.Add(total_outlets == N)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
    # Optional: print the allocation
    for i in R:
        for k in K:
            if x[i, k].solution_value() > 0.5:
                print(f"Region {i+1} gets {k} outlets")
else:
    print("NO_FEASIBLE_SOLUTION")