from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Index sets
I = [1, 2]
J = [1, 2, 3]

# Cost matrix C[i][j]
C = dict()
C[1, 1] = 15
C[1, 2] = 18
C[1, 3] = 22
C[2, 1] = 21
C[2, 2] = 25
C[2, 3] = 16

# Supply capacities
S = dict()
S[1] = 400
S[2] = 450

# Demand bounds
D_min = dict()
D_min[1] = 290
D_min[2] = 250
D_min[3] = 270

D_max = dict()
D_max[1] = 320
D_max[2] = 250
D_max[3] = 350

# Decision variables x[i, j] >= 0
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

# Objective: minimize total cost
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(C[i, j] * x[i, j])
solver.Minimize(sum(obj_terms))

# Supply constraints: all electricity used (equality)
for i in I:
    supply_expr = sum(x[i, j] for j in J)
    solver.Add(supply_expr == S[i])

# Demand constraints: min <= flow <= max
for j in J:
    demand_expr = sum(x[i, j] for i in I)
    solver.Add(demand_expr >= D_min[j])
    solver.Add(demand_expr <= D_max[j])

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")