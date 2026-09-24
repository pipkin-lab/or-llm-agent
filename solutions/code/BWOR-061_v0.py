from ortools.linear_solver import pywraplp

# Parameters
p = dict()
p[1] = 0.30
p[2] = 0.50
p[3] = 0.20

v = dict()
v[1] = 1
v[2] = 2
v[3] = 3

# E3 is the expected value of the forced-hire 3rd candidate
E3 = p[1] * v[1] + p[2] * v[2] + p[3] * v[3]

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables: x[i][q] = 1 if hire candidate i given score q
# Only decision nodes are (1,2), (1,3), (2,2), (2,3)
x = dict()
for i in [1, 2]:
    for q in [2, 3]:
        x[(i, q)] = solver.BoolVar('x_%d_%d' % (i, q))

# V[i][q]: expected value from state (candidate i, observed score q)
V = dict()
for i in [1, 2]:
    for q in [1, 2, 3]:
        V[(i, q)] = solver.NumVar(0, INF, 'V_%d_%d' % (i, q))

# E2: expected value entering candidate 2
E2 = solver.NumVar(0, INF, 'E2')

# --- Stage 3 (forced hire) is captured by the constant E3 ---

# --- Stage 2 constraints ---
# V[2][1] = E3 (must reject score 1)
solver.Add(V[(2, 1)] == E3)

# V[2][2] = 2*x[2][2] + E3*(1 - x[2][2])
# i.e., V[2][2] = E3 + (2 - E3)*x[2][2]
solver.Add(V[(2, 2)] == E3 + (2 - E3) * x[(2, 2)])

# V[2][3] = 3*x[2][3] + E3*(1 - x[2][3])
# i.e., V[2][3] = E3 + (3 - E3)*x[2][3]
solver.Add(V[(2, 3)] == E3 + (3 - E3) * x[(2, 3)])

# E2 = 0.3*V[2][1] + 0.5*V[2][2] + 0.2*V[2][3]
solver.Add(E2 == p[1] * V[(2, 1)] + p[2] * V[(2, 2)] + p[3] * V[(2, 3)])

# --- Stage 1 constraints ---
# V[1][1] = E2 (must reject score 1)
solver.Add(V[(1, 1)] == E2)

# V[1][2] = 2*x[1][2] + E2*(1 - x[1][2])
# i.e., V[1][2] = E2 + (2 - E2)*x[1][2]
solver.Add(V[(1, 2)] == E2 + (2 - E2) * x[(1, 2)])

# V[1][3] = 3*x[1][3] + E2*(1 - x[1][3])
# i.e., V[1][3] = E2 + (3 - E2)*x[1][3]
solver.Add(V[(1, 3)] == E2 + (3 - E2) * x[(1, 3)])

# Objective: Z = 0.3*V[1][1] + 0.5*V[1][2] + 0.2*V[1][3]
objective = p[1] * V[(1, 1)] + p[2] * V[(1, 2)] + p[3] * V[(1, 3)]
solver.Maximize(objective)

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")