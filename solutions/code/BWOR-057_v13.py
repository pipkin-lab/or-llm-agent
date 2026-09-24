from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

INF = solver.infinity()

# Sets and parameters
I = [1, 2, 3, 4, 5, 6]
D = dict()
D[1] = 500
D[2] = 550
D[3] = 700
D[4] = 900
D[5] = 400
D[6] = 300

C = dict()
C[1] = 5
C[2] = 8
C[3] = 10
C[4] = 12
C[5] = 16
C[6] = 18

F = 1200

M = dict()
M[1] = 3350
M[2] = 2850
M[3] = 2300
M[4] = 1600
M[5] = 700
M[6] = 300

# Decision variables
x = dict()
for i in I:
    x[i] = solver.IntVar(0, INF, 'x_' + str(i))

y = dict()
for i in I:
    y[i] = solver.BoolVar('y_' + str(i))

# Objective function
obj_terms = []
for i in I:
    obj_terms.append(C[i] * x[i] + F * y[i])
solver.Minimize(sum(obj_terms))

# Cumulative demand constraints
for i in I:
    expr = sum(x[j] for j in I if j >= i)
    solver.Add(expr >= D[i])

# Machine activation constraints
for i in I:
    solver.Add(x[i] <= M[i] * y[i])

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")