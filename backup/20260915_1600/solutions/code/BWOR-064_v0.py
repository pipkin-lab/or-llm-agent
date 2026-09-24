from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('SCIP')

# Index sets
I = [1, 2, 3]
J = {
    1: [0, 1, 2],
    2: [0, 1, 2, 3],
    3: [0, 1]
}

# Parameters: C[i][j] investment cost, R[i][j] return
C = dict()
C[1] = dict(); C[1][0] = 0; C[1][1] = 1; C[1][2] = 2
C[2] = dict(); C[2][0] = 0; C[2][1] = 2; C[2][2] = 3; C[2][3] = 4
C[3] = dict(); C[3][0] = 0; C[3][1] = 1

R = dict()
R[1] = dict(); R[1][0] = 0; R[1][1] = 5; R[1][2] = 6
R[2] = dict(); R[2][0] = 0; R[2][1] = 8; R[2][2] = 9; R[2][3] = 12
R[3] = dict(); R[3][0] = 0; R[3][1] = 3

B = 5

# Decision variables: x[i][j] binary
x = dict()
for i in I:
    x[i] = dict()
    for j in J[i]:
        x[i][j] = solver.BoolVar('x_' + str(i) + '_' + str(j))

# Objective: maximize total return
obj_terms = []
for i in I:
    for j in J[i]:
        obj_terms.append(R[i][j] * x[i][j])
solver.Maximize(sum(obj_terms))

# Budget constraint
budget_terms = []
for i in I:
    for j in J[i]:
        budget_terms.append(C[i][j] * x[i][j])
solver.Add(sum(budget_terms) <= B)

# Single plan selection per factory
for i in I:
    solver.Add(sum(x[i][j] for j in J[i]) == 1)

# Solve
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print("OPTIMAL_VALUE:", solver.Objective().Value())
else:
    print("NO_FEASIBLE_SOLUTION")