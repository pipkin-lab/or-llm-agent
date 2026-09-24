from ortools.linear_solver import pywraplp

# Parameters
periods = [1, 2, 3, 4, 5, 6]
demand = dict()
demand[1] = 100
demand[2] = 70
demand[3] = 80
demand[4] = 120
demand[5] = 150
demand[6] = 140

c_N = 10
c_F = 2
c_S = 10

# Solver
solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Decision variables
N = dict()
F = dict()
S = dict()

for t in periods:
    N[t] = solver.NumVar(0, INF, 'N_' + str(t))
    F[t] = solver.NumVar(0, INF, 'F_' + str(t))
    S[t] = solver.NumVar(0, INF, 'S_' + str(t))

# Objective
obj = 0
for t in periods:
    obj += c_N * N[t] + c_F * F[t] + c_S * S[t]

# Demand satisfaction constraints
for t in periods:
    expr = N[t]
    if t >= 2:
        expr += F[t - 1]
    if t >= 3:
        expr += S[t - 2]
    solver.Add(expr >= demand[t])

# Solve
solver.Minimize(obj)
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")