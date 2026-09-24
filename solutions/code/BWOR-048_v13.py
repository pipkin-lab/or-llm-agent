from ortools.linear_solver import pywraplp

# Parameters
T = 6
D = {1: 100, 2: 70, 3: 80, 4: 120, 5: 150, 6: 140}
C_new = 10
C_fast = 2
C_slow = 10

# Cumulative demand
D_cum = dict()
running = 0
for t in range(1, T + 1):
    running += D[t]
    D_cum[t] = running

# Solver
solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision Variables
x = dict()
f = dict()
s = dict()

for t in range(1, T + 1):
    x[t] = solver.IntVar(0, INF, 'x_' + str(t))
    f[t] = solver.IntVar(0, INF, 'f_' + str(t))
    s[t] = solver.IntVar(0, INF, 's_' + str(t))

# Objective
obj = 0
for t in range(1, T + 1):
    obj += C_new * x[t] + C_fast * f[t] + C_slow * s[t]

solver.Minimize(obj)

# Demand Satisfaction Constraints
# t=1: x_1 = D_1
solver.Add(x[1] == D[1])
# t=2: x_2 + f_1 = D_2
solver.Add(x[2] + f[1] == D[2])
# t=3: x_3 + f_2 + s_1 = D_3
solver.Add(x[3] + f[2] + s[1] == D[3])
# t=4: x_4 + f_3 + s_2 = D_4
solver.Add(x[4] + f[3] + s[2] == D[4])
# t=5: x_5 + f_4 + s_3 = D_5
solver.Add(x[5] + f[4] + s[3] == D[5])
# t=6: x_6 + f_5 + s_4 = D_6
solver.Add(x[6] + f[5] + s[4] == D[6])

# Used Engine Availability Constraints
# For each t: sum_{i=1}^t f_i + sum_{i=1}^t s_i <= D_cum[t]
for t in range(1, T + 1):
    lhs = 0
    for i in range(1, t + 1):
        lhs += f[i] + s[i]
    solver.Add(lhs <= D_cum[t])

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")