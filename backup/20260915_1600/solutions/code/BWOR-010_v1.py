from ortools.linear_solver import pywraplp

I = [1, 2, 3]
J = [1, 2, 3]

S = {1: 20, 2: 30, 3: 20}
D = {1: 15, 2: 25, 3: 20}

c = {
    (1, 1): 3, (1, 2): 10, (1, 3): 2,
    (2, 1): 4, (2, 2): 11, (2, 3): 8,
    (3, 1): 8, (3, 2): 11, (3, 3): 4
}

p = {1: 12, 2: 16, 3: 11}

b = dict()
for i in I:
    for j in J:
        b[i, j] = p[j] - c[i, j]

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

obj = 0
for i in I:
    for j in J:
        obj += b[i, j] * x[i, j]

solver.Maximize(obj)

for i in I:
    solver.Add(sum(x[i, j] for j in J) <= S[i])

for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")