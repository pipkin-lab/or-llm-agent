from ortools.linear_solver import pywraplp

# Profit tables for each region (index 0 to 4)
P1 = {0: 0, 1: 16, 2: 25, 3: 30, 4: 32}
P2 = {0: 0, 1: 12, 2: 17, 3: 21, 4: 22}
P3 = {0: 0, 1: 10, 2: 14, 3: 16, 4: 17}

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x1, x2, x3 are non-negative integers, each <= 4
x1 = solver.IntVar(0, 4, 'x1')
x2 = solver.IntVar(0, 4, 'x2')
x3 = solver.IntVar(0, 4, 'x3')

# Constraint: exactly 4 outlets total
solver.Add(x1 + x2 + x3 == 4)

# Since the objective is non-linear (table lookup), we use a standard
# approach: enumerate all feasible integer combinations and pick the best.
# However, OR-Tools MILP cannot directly handle table-based non-linear objectives.
# So we solve by enumerating the small feasible set.

best_profit = -1
best_alloc = None

for xv1 in range(5):
    for xv2 in range(5):
        xv3 = 4 - xv1 - xv2
        if xv3 < 0 or xv3 > 4:
            continue
        profit = P1[xv1] + P2[xv2] + P3[xv3]
        if profit > best_profit:
            best_profit = profit
            best_alloc = (xv1, xv2, xv3)

print("OPTIMAL_VALUE:", best_profit)