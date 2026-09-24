from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')
INF = solver.infinity()

I = [1, 2, 3]
J = ['A', 'B', 'C']

c = dict()
c[1, 'A'] = 1
c[1, 'B'] = 2
c[1, 'C'] = 2
c[2, 'A'] = 1
c[2, 'B'] = 4
c[2, 'C'] = 5
c[3, 'A'] = 2
c[3, 'B'] = 3
c[3, 'C'] = 3

S = dict()
S[1] = 20
S[2] = 40
S[3] = 30

D = dict()
D['A'] = 30
D['B'] = 20
D['C'] = 20

h = dict()
h[1] = 5
h[2] = 4
h[3] = 3

MinShip = dict()
MinShip[1] = 0
MinShip[2] = 38
MinShip[3] = 27

x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, INF, 'x_' + str(i) + '_' + j)

# Objective: sum c_ij * x_ij + sum h_i * (S_i - sum_j x_ij)
obj = 0
for i in I:
    for j in J:
        obj += c[i, j] * x[i, j]
    obj += h[i] * (S[i] - sum(x[i, j] for j in J))

solver.Minimize(obj)

# Supply constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) <= S[i])

# Demand constraints
for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

# Minimum shipment constraints
for i in I:
    solver.Add(sum(x[i, j] for j in J) >= MinShip[i])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")