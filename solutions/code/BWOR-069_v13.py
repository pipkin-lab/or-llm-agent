from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Parameters
w = dict()
w[1] = 2
w[2] = 3
w[3] = 4

p = dict()
p[1] = 100
p[2] = 140
p[3] = 180

W_max = 10

# Index set
I = [1, 2, 3]

# Decision variables: x_i (integer, non-negative)
x = dict()
for i in I:
    x[i] = solver.IntVar(0, solver.infinity(), 'x_' + str(i))

# Objective: Maximize total profit
obj = sum(p[i] * x[i] for i in I)
solver.Maximize(obj)

# Transportation capacity constraint
solver.Add(sum(w[i] * x[i] for i in I) <= W_max)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")