from ortools.linear_solver import pywraplp

# Parameters
D = dict()
D[1] = 1500
D[2] = 1000
D[3] = 2000
D[4] = 1200

C = dict()
C[1] = 28
C[2] = 45
C[3] = 60
C[4] = 73

I = [1, 2, 3, 4]
K = [1, 2, 3, 4]

# Valid (i, k) pairs: i + k - 1 <= 4
valid_pairs = dict()
for i in I:
    for k in K:
        if i + k - 1 <= 4:
            valid_pairs[(i, k)] = True

# Create solver (MILP, but variables are continuous; GLOP can handle LP, SCIP for MILP)
# Since x_{i,k} are continuous, use GLOP
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables x[i, k]
x = dict()
for i in I:
    for k in K:
        if (i, k) in valid_pairs:
            x[i, k] = solver.NumVar(0, INF, 'x_{}_{}'.format(i, k))

# Objective: minimize total cost
obj_terms = []
for i in I:
    for k in K:
        if (i, k) in valid_pairs:
            obj_terms.append(C[k] * x[i, k])
solver.Minimize(sum(obj_terms))

# Constraints: for each month t, total active space >= D[t]
for t in I:
    active_terms = []
    for i in I:
        for k in K:
            if (i, k) in valid_pairs:
                # Contract (i, k) is active in month t if i <= t <= i + k - 1
                if i <= t <= i + k - 1:
                    active_terms.append(x[i, k])
    solver.Add(sum(active_terms) >= D[t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")