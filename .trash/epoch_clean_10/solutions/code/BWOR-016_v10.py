from ortools.linear_solver import pywraplp

# Parameters
c = {
    (1, 1): 2, (1, 2): 9, (1, 3): 3, (1, 4): 4,
    (2, 1): 8, (2, 2): 3, (2, 3): 5, (2, 4): 7,
    (3, 1): 7, (3, 2): 6, (3, 3): 1, (3, 4): 2,
    (4, 1): 4, (4, 2): 5, (4, 3): 2, (4, 4): 5
}

S = {1: 400, 2: 600, 3: 200, 4: 200}
D = {1: 350, 2: 400, 3: 300, 4: 150}
F = {1: 0, 2: 0, 3: 1200, 4: 1500}

I = [1, 2, 3, 4]
J = [1, 2, 3, 4]

# Create solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if solver is None:
    print("Could not create solver")
    exit(1)

# Decision variables
# x[i, j] >= 0
x = dict()
for i in I:
    for j in J:
        x[i, j] = solver.NumVar(0, solver.infinity(), 'x_' + str(i) + '_' + str(j))

# y[i] binary for i in {3, 4}
y = dict()
for i in [3, 4]:
    y[i] = solver.IntVar(0, 1, 'y_' + str(i))

# Objective: minimize sum c_ij x_ij + F_3 y_3 + F_4 y_4
obj_terms = []
for i in I:
    for j in J:
        obj_terms.append(c[(i, j)] * x[i, j])
obj_terms.append(F[3] * y[3])
obj_terms.append(F[4] * y[4])

solver.Minimize(sum(obj_terms))

# Demand satisfaction constraints: sum_i x[i, j] == D[j]
for j in J:
    solver.Add(sum(x[i, j] for i in I) == D[j])

# Capacity constraints:
# i=1: sum_j x[1,j] <= 400
# i=2: sum_j x[2,j] <= 600
# i=3: sum_j x[3,j] <= 200 * y[3]
# i=4: sum_j x[4,j] <= 200 * y[4]
solver.Add(sum(x[1, j] for j in J) <= S[1])
solver.Add(sum(x[2, j] for j in J) <= S[2])
solver.Add(sum(x[3, j] for j in J) <= S[3] * y[3])
solver.Add(sum(x[4, j] for j in J) <= S[4] * y[4])

# Facility selection constraint: y[3] + y[4] == 1
solver.Add(y[3] + y[4] == 1)

# Solve
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")