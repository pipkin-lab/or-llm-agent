from ortools.linear_solver import pywraplp

# Parameter: c[a][s] = time for athlete a to swim stroke s
# Strokes: 1=Backstroke, 2=Breaststroke, 3=Butterfly, 4=Freestyle
# Athletes: 1=Zhao, 2=Qian, 3=Zhang, 4=Wang, 5=Zhou
c = dict()
c[1, 1] = 37.7
c[1, 2] = 43.4
c[1, 3] = 33.3
c[1, 4] = 29.2

c[2, 1] = 32.9
c[2, 2] = 33.1
c[2, 3] = 28.5
c[2, 4] = 26.4

c[3, 1] = 33.8
c[3, 2] = 42.2
c[3, 3] = 38.9
c[3, 4] = 29.6

c[4, 1] = 37.0
c[4, 2] = 34.7
c[4, 3] = 30.4
c[4, 4] = 28.5

c[5, 1] = 35.4
c[5, 2] = 41.8
c[5, 3] = 33.6
c[5, 4] = 31.1

# Index sets
S = [1, 2, 3, 4]
A = [1, 2, 3, 4, 5]

# Create solver (MILP)
solver = pywraplp.Solver.CreateSolver('SCIP')

# Decision variables x[a, s]
x = dict()
for a in A:
    for s in S:
        x[a, s] = solver.BoolVar('x_' + str(a) + '_' + str(s))

# Objective: minimize total time
obj = 0
for a in A:
    for s in S:
        obj += c[a, s] * x[a, s]

solver.Minimize(obj)

# Constraint 1: Each stroke assigned to exactly one athlete
for s in S:
    solver.Add(sum(x[a, s] for a in A) == 1)

# Constraint 2: Each athlete at most one stroke
for a in A:
    solver.Add(sum(x[a, s] for s in S) <= 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")