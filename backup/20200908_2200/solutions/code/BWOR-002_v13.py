from ortools.linear_solver import pywraplp

# Data
I = [1, 2, 3, 4, 5]
p = {1: 3, 2: 2, 3: 1, 4: 6, 5: 18}
m = {1: 1.0, 2: 0.5, 3: 0.2, 4: 2.0, 5: 0.5}
v = {1: 0.5, 2: 1.0, 3: 0.2, 4: 2.0, 5: 0.8}
c = {1: 0.2, 2: 0.7, 3: 0.4, 4: 0.3, 5: 0.8}

P_req = 700
M_req = 30
V_req = 100

# Solver
solver = pywraplp.Solver.CreateSolver('GLOP')

# Variables
x = dict()
for i in I:
    x[i] = solver.NumVar(0, solver.infinity(), 'x_' + str(i))

# Objective
obj = 0
for i in I:
    obj += c[i] * x[i]
solver.Minimize(obj)

# Constraints
solver.Add(sum(p[i] * x[i] for i in I) >= P_req)
solver.Add(sum(m[i] * x[i] for i in I) >= M_req)
solver.Add(sum(v[i] * x[i] for i in I) >= V_req)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")