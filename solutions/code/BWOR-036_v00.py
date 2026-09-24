from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

n = 4
t = [1, 2, 3, 4]

x = dict()
s = dict()
I = dict()

for t_val in t:
    x[t_val] = solver.NumVar(0, INF, 'x_' + str(t_val))
    s[t_val] = solver.NumVar(0, INF, 's_' + str(t_val))
    I[t_val] = solver.NumVar(0, INF, 'I_' + str(t_val))

c = dict()
c[1] = 410
c[2] = 430
c[3] = 460
c[4] = 450

p = dict()
p[1] = 425
p[2] = 440
p[3] = 465
p[4] = 455

Smax = dict()
Smax[1] = 100
Smax[2] = 140
Smax[3] = 200
Smax[4] = 160

# Objective: Maximize profit
obj = 0
for t_val in t:
    obj += p[t_val] * s[t_val]
    obj -= c[t_val] * x[t_val]

# Storage costs: 170*I_1 + 100*I_2 + 100*I_3
obj -= 170 * I[1]
obj -= 100 * I[2]
obj -= 100 * I[3]

solver.Maximize(obj)

# Inventory balance constraints
solver.Add(x[1] - s[1] == I[1])
solver.Add(x[2] - s[2] + I[1] == I[2])
solver.Add(x[3] - s[3] + I[2] == I[3])
solver.Add(x[4] - s[4] + I[3] == 0)  # I_4 = 0

# Sales capacity constraints
for t_val in t:
    solver.Add(s[t_val] <= Smax[t_val])

# Warehouse capacity constraints
for t_val in [1, 2, 3]:
    solver.Add(I[t_val] <= 20)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")