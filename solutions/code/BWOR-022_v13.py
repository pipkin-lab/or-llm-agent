from ortools.linear_solver import pywraplp

# Parameters
C = [1, 2, 3]
K = [1, 2, 3]
B = 8

# Cost c[c][k]
cost = dict()
cost[1, 1] = 1
cost[1, 2] = 2
cost[1, 3] = 3
cost[2, 1] = 3
cost[2, 2] = 5
cost[2, 3] = 6
cost[3, 1] = 2
cost[3, 2] = 3
cost[3, 3] = 4

# log reliability ln(r[c][k])
logr = dict()
logr[1, 1] = -1.2040
logr[1, 2] = -0.9163
logr[1, 3] = -0.6931
logr[2, 1] = -1.6094
logr[2, 2] = -0.6931
logr[2, 3] = -0.1054
logr[3, 1] = -2.3026
logr[3, 2] = -1.6094
logr[3, 3] = -0.3567

# Solver (MILP)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[c][k] binary
x = dict()
for c in C:
    for k in K:
        x[c, k] = solver.BoolVar('x_' + str(c) + '_' + str(k))

# Constraint 1: Allocation uniqueness
for c in C:
    solver.Add(sum(x[c, k] for k in K) == 1)

# Constraint 2: Budget
solver.Add(sum(cost[c, k] * x[c, k] for c in C for k in K) <= B)

# Objective: maximize sum of log reliabilities
obj = sum(logr[c, k] * x[c, k] for c in C for k in K)
solver.Maximize(obj)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")