from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
I = [1, 2, 3, 4]
w = dict()
w[1] = 2
w[2] = 3
w[3] = 4
w[4] = 5

v = dict()
v[1] = 2
v[2] = 2
v[3] = 2
v[4] = 3

c = dict()
c[1] = 3
c[2] = 4
c[3] = 5
c[4] = 6

W_max = 15
V_max = 10

# Decision variables
x = dict()
for i in I:
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

# Objective function
obj = sum(c[i] * x[i] for i in I)
solver.Maximize(obj)

# Constraints
solver.Add(sum(w[i] * x[i] for i in I) <= W_max)
solver.Add(sum(v[i] * x[i] for i in I) <= V_max)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")