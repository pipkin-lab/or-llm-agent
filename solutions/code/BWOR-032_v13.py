from ortools.linear_solver import pywraplp

# Parameters
T = list(range(1, 13))
I = [1, 2]

C = 120000
v = {1: 0.2, 2: 0.4}
W = 15000
h = 1.0
h_e = 1.5

d = {
    1: {1: 10000, 2: 50000, 3: 10000, 4: 10000, 5: 30000, 6: 30000, 7: 30000, 8: 30000, 9: 30000, 10: 100000, 11: 100000, 12: 100000},
    2: {1: 50000, 2: 50000, 3: 15000, 4: 15000, 5: 15000, 6: 15000, 7: 15000, 8: 15000, 9: 15000, 10: 50000, 11: 50000, 12: 50000}
}

c = {
    1: {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 4.5, 7: 4.5, 8: 4.5, 9: 4.5, 10: 4.5, 11: 4.5, 12: 4.5},
    2: {1: 8, 2: 8, 3: 8, 4: 8, 5: 8, 6: 7, 7: 7, 8: 7, 9: 7, 10: 7, 11: 7, 12: 7}
}

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

# Decision variables
x = dict()
for i in I:
    for t in T:
        x[i, t] = solver.NumVar(0, INF, 'x_{}_{}'.format(i, t))

Inv = dict()
for i in I:
    for t in T:
        Inv[i, t] = solver.NumVar(0, INF, 'Inv_{}_{}'.format(i, t))

E = dict()
for t in T:
    E[t] = solver.NumVar(0, INF, 'E_{}'.format(t))

U = dict()
for t in T:
    U[t] = solver.NumVar(0, W, 'U_{}'.format(t))

# Objective
obj_terms = []
for t in T:
    for i in I:
        obj_terms.append(c[i][t] * x[i, t])
    obj_terms.append(h * U[t])
    obj_terms.append(h_e * E[t])
solver.Minimize(sum(obj_terms))

# Constraints

# (1) Inventory balance
for i in I:
    for t in T:
        if t == 1:
            solver.Add(Inv[i, t] == x[i, t] - d[i][t])
        else:
            solver.Add(Inv[i, t] == Inv[i, t - 1] + x[i, t] - d[i][t])

# (2) Monthly production capacity
for t in T:
    solver.Add(x[1, t] + x[2, t] <= C)

# (3) Total warehouse volume must accommodate inventory
for t in T:
    solver.Add(v[1] * Inv[1, t] + v[2] * Inv[2, t] <= W + E[t])

# (4) In-house warehouse volume used U_t
for t in T:
    solver.Add(U[t] <= W)
    solver.Add(U[t] <= v[1] * Inv[1, t] + v[2] * Inv[2, t])
    solver.Add(U[t] + E[t] == v[1] * Inv[1, t] + v[2] * Inv[2, t])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")