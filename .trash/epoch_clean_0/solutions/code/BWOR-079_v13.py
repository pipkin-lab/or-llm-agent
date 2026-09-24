from ortools.linear_solver import pywraplp

# Index sets (1-indexed as per model)
D = [1, 2, 3, 4, 5, 6, 7]  # Days
P = [1, 2, 3, 4, 5]        # Periods
K = [1, 2, 3, 4, 5, 6, 7]  # Start days

# Requirements R_p (1-indexed)
R = dict()
R[1] = 18
R[2] = 20
R[3] = 19
R[4] = 17
R[5] = 12

# Coverage matrix a[s, p]: shift s covers period p
# Shifts 1-5, Periods 1-5
a = dict()
a[1, 1] = 1
a[1, 2] = 0
a[1, 3] = 0
a[1, 4] = 0
a[1, 5] = 1
a[2, 1] = 1
a[2, 2] = 1
a[2, 3] = 0
a[2, 4] = 0
a[2, 5] = 0
a[3, 1] = 0
a[3, 2] = 1
a[3, 3] = 1
a[3, 4] = 0
a[3, 5] = 0
a[4, 1] = 0
a[4, 2] = 0
a[4, 3] = 1
a[4, 4] = 1
a[4, 5] = 0
a[5, 1] = 0
a[5, 2] = 0
a[5, 3] = 0
a[5, 4] = 1
a[5, 5] = 1

# Pre-compute c[d, p, k] coefficients
# c[d, p, k] = 1 if nurse starting on day k is working on day d AND their shift on day d covers period p
c = dict()
for d in D:
    for p in P:
        for k in K:
            diff = (d - k) % 7
            if diff <= 4:
                s = diff + 1  # shift assigned
                c[d, p, k] = a[s, p]
            else:
                c[d, p, k] = 0

# Create MILP solver
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables: x[k] for k in K (integer, non-negative)
x = dict()
for k in K:
    x[k] = solver.IntVar(0, solver.infinity(), 'x_' + str(k))

# Objective: Minimize sum of x[k]
obj = sum(x[k] for k in K)
solver.Minimize(obj)

# Constraints: for each day d and period p, sum of c[d,p,k]*x[k] >= R[p]
for d in D:
    for p in P:
        expr = sum(c[d, p, k] * x[k] for k in K)
        solver.Add(expr >= R[p])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")