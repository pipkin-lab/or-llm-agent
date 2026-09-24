from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets: shifts 1-6, blocks 1-6
S = range(1, 7)
B = range(1, 7)

# Parameters
c_FT = 80
c_CT = 120
d = dict()
d[1] = 10
d[2] = 15
d[3] = 25
d[4] = 20
d[5] = 18
d[6] = 12

# Shift-block incidence: a[s, b] = 1 if shift s covers block b
a = dict()
a[1, 1] = 1
a[1, 2] = 1
a[2, 2] = 1
a[2, 3] = 1
a[3, 3] = 1
a[3, 4] = 1
a[4, 4] = 1
a[4, 5] = 1
a[5, 5] = 1
a[5, 6] = 1
a[6, 6] = 1
a[6, 1] = 1

# Decision variables
x = dict()
y = dict()
for s in S:
    x[s] = solver.IntVar(0, solver.infinity(), 'x_' + str(s))
    y[s] = solver.IntVar(0, solver.infinity(), 'y_' + str(s))

# Objective: minimize total cost
obj_terms = []
for s in S:
    obj_terms.append(c_FT * x[s])
    obj_terms.append(c_CT * y[s])
obj = sum(obj_terms)
solver.Minimize(obj)

# Coverage constraints
for b in B:
    coverage = 0
    for s in S:
        if (s, b) in a and a[s, b] == 1:
            coverage += x[s] + y[s]
    solver.Add(coverage >= d[b])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")