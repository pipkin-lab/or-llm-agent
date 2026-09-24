from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Parameters
c = dict()
c[1] = 0.20
c[2] = 0.70
c[3] = 0.40
c[4] = 0.30
c[5] = 0.80

p = dict()
p[1] = 3
p[2] = 2
p[3] = 1
p[4] = 6
p[5] = 18

m = dict()
m[1] = 1.0
m[2] = 0.5
m[3] = 0.2
m[4] = 2.0
m[5] = 0.5

v = dict()
v[1] = 0.5
v[2] = 1.0
v[3] = 0.2
v[4] = 2.0
v[5] = 0.8

P_req = 700
M_req = 30
V_req = 100

# Decision variables
x = dict()
for i in range(1, 6):
    x[i] = solver.NumVar(0, solver.infinity(), 'x_' + str(i))

# Objective: minimize cost
obj = c[1] * x[1] + c[2] * x[2] + c[3] * x[3] + c[4] * x[4] + c[5] * x[5]
solver.Minimize(obj)

# Constraints
solver.Add(p[1] * x[1] + p[2] * x[2] + p[3] * x[3] + p[4] * x[4] + p[5] * x[5] >= P_req)
solver.Add(m[1] * x[1] + m[2] * x[2] + m[3] * x[3] + m[4] * x[4] + m[5] * x[5] >= M_req)
solver.Add(v[1] * x[1] + v[2] * x[2] + v[3] * x[3] + v[4] * x[4] + v[5] * x[5] >= V_req)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")