from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

# Parameter definitions
I = [1, 2, 3]
J = [1, 2, 3]

# Net benefit coefficients b_ij = p_j - c_ij
b = dict()
b[1, 1] = 9
b[1, 2] = 6
b[1, 3] = 9
b[2, 1] = 8
b[2, 2] = 5
b[2, 3] = 3
b[3, 1] = 4
b[3, 2] = 5
b[3, 3] = 7

# Supply capacities S_i
S = dict()
S[1] = 20
S[2] = 30
S[3] = 20

# Demand capacities D_j
D = dict()
D[1] = 15
D[2] = 25
D[3] = 20

# Decision variables x_ij
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + str(j))

# Objective: Maximize total net benefit
obj = 0
for i in I:
    for j in J:
        obj += b[i, j] * x[i, j]

solver.Maximize(obj)

# Supply constraints: sum_j x_ij <= S_i
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= S[i])

# Demand constraints: sum_i x_ij <= D_j
for j in J:
    solver.Add(sum(x[i, j] for i in I) <= D[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")