from ortools.linear_solver import pywraplp

# Index sets
I = [1, 2, 3, 4, 5, 6]
I_UG = [1, 2, 3, 4]
I_Grad = [5, 6]
T = [1, 2, 3, 4, 5]

# Parameters
w = dict()
w[1] = 10.0
w[2] = 10.0
w[3] = 9.9
w[4] = 9.8
w[5] = 10.8
w[6] = 11.3

H = dict()
# Student 1 (UG)
H[1, 1] = 6
H[1, 2] = 0
H[1, 3] = 9
H[1, 4] = 0
H[1, 5] = 7
# Student 2 (UG)
H[2, 1] = 0
H[2, 2] = 9
H[2, 3] = 0
H[2, 4] = 6
H[2, 5] = 0
# Student 3 (UG)
H[3, 1] = 4
H[3, 2] = 8
H[3, 3] = 3
H[3, 4] = 0
H[3, 5] = 5
# Student 4 (UG)
H[4, 1] = 5
H[4, 2] = 5
H[4, 3] = 6
H[4, 4] = 0
H[4, 5] = 4
# Student 5 (Grad)
H[5, 1] = 3
H[5, 2] = 0
H[5, 3] = 4
H[5, 4] = 8
H[5, 5] = 0
# Student 6 (Grad)
H[6, 1] = 0
H[6, 2] = 9
H[6, 3] = 0
H[6, 4] = 6
H[6, 5] = 3

D = dict()
for t in T:
    D[t] = 14

MinH_UG = 8
MinH_Grad = 7

# Solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables: x[i, t] continuous >= 0, bounded by H[i, t]
x = dict()
for i in I:
    for t in T:
        x[i, t] = solver.NumVar(0, H[i, t], 'x_' + str(i) + '_' + str(t))

# Objective: Minimize total wage
obj = 0
for i in I:
    for t in T:
        obj += w[i] * x[i, t]
solver.Minimize(obj)

# Constraint 1: Daily coverage
for t in T:
    solver.Add(sum(x[i, t] for i in I) == D[t])

# Constraint 2: Availability (already enforced via variable upper bounds)

# Constraint 3: Minimum weekly work hours
for i in I_UG:
    solver.Add(sum(x[i, t] for t in T) >= MinH_UG)
for i in I_Grad:
    solver.Add(sum(x[i, t] for t in T) >= MinH_Grad)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")