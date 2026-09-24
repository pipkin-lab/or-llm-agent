from ortools.linear_solver import pywraplp

# Define index sets
I = [1, 2, 3, 4]       # Undergraduate students
G = [5, 6]              # Graduate students
K = [1, 2, 3, 4, 5, 6] # All students
D = [1, 2, 3, 4, 5]    # Days (1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri)

# Parameters
w = dict()
w[1] = 10.0
w[2] = 10.0
w[3] = 9.9
w[4] = 9.8
w[5] = 10.8
w[6] = 11.3

M = dict()
M[1, 1] = 6
M[1, 2] = 0
M[1, 3] = 9
M[1, 4] = 0
M[1, 5] = 7
M[2, 1] = 0
M[2, 2] = 9
M[2, 3] = 0
M[2, 4] = 6
M[2, 5] = 0
M[3, 1] = 4
M[3, 2] = 8
M[3, 3] = 3
M[3, 4] = 0
M[3, 5] = 5
M[4, 1] = 5
M[4, 2] = 5
M[4, 3] = 6
M[4, 4] = 0
M[4, 5] = 4
M[5, 1] = 3
M[5, 2] = 0
M[5, 3] = 4
M[5, 4] = 8
M[5, 5] = 0
M[6, 1] = 0
M[6, 2] = 9
M[6, 3] = 0
M[6, 4] = 6
M[6, 5] = 3

H = 14
L_U = 8
L_G = 7

# Create LP solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Create decision variables x[k, d]
x = dict()
for k in K:
    for d in D:
        x[k, d] = solver.NumVar(0, INF, 'x_' + str(k) + '_' + str(d))

# Objective function: Minimize total wage
obj = 0
for k in K:
    for d in D:
        obj += w[k] * x[k, d]
solver.Minimize(obj)

# Constraint 1: Daily coverage - sum of hours on each day must equal 14
for d in D:
    solver.Add(sum(x[k, d] for k in K) == H)

# Constraint 2: Maximum availability per student per day
for k in K:
    for d in D:
        solver.Add(x[k, d] <= M[k, d])

# Constraint 3: Minimum weekly hours for undergraduates
for k in I:
    solver.Add(sum(x[k, d] for d in D) >= L_U)

# Constraint 4: Minimum weekly hours for graduates
for k in G:
    solver.Add(sum(x[k, d] for d in D) >= L_G)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")