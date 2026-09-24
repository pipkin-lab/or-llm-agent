from ortools.linear_solver import pywraplp

# Parameter values from Table 5-2
# c[s][a] where s in {1,2,3,4}, a in {1,2,3,4,5}
c = dict()
c[1] = dict()
c[1][1] = 37.7
c[1][2] = 32.9
c[1][3] = 33.8
c[1][4] = 37.0
c[1][5] = 35.4
c[2] = dict()
c[2][1] = 43.4
c[2][2] = 33.1
c[2][3] = 42.2
c[2][4] = 34.7
c[2][5] = 41.8
c[3] = dict()
c[3][1] = 33.3
c[3][2] = 28.5
c[3][3] = 38.9
c[3][4] = 30.4
c[3][5] = 33.6
c[4] = dict()
c[4][1] = 29.2
c[4][2] = 26.4
c[4][3] = 29.6
c[4][4] = 28.5
c[4][5] = 31.1

S = [1, 2, 3, 4]
A = [1, 2, 3, 4, 5]

solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[s][a]
x = dict()
for s in S:
    for a in A:
        x[s, a] = solver.BoolVar('x_' + str(s) + '_' + str(a))

# Objective: minimize total time
obj_terms = []
for s in S:
    for a in A:
        obj_terms.append(c[s][a] * x[s, a])
solver.Minimize(sum(obj_terms))

# Constraint 1: Each stroke assigned to exactly one athlete
for s in S:
    solver.Add(sum(x[s, a] for a in A) == 1)

# Constraint 2: Each athlete swims at most one stroke
for a in A:
    solver.Add(sum(x[s, a] for s in S) <= 1)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")